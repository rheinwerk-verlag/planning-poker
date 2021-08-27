from unittest.mock import Mock, patch

from channels.db import database_sync_to_async
from channels.testing import WebsocketCommunicator
import pytest

from example.asgi import application


class TestPokerConsumer:
    def test_poker_session(self, poker_consumer, poker_session):
        assert poker_consumer.poker_session.id == poker_session.id

    @pytest.mark.asyncio
    @pytest.mark.django_db(transaction=True)
    @pytest.mark.parametrize('has_active_story', [True, False])
    async def test_connect(self, has_active_story, poker_session, story):
        if has_active_story:
            poker_session.active_story = story
            await database_sync_to_async(poker_session.save)()
        communicator = WebsocketCommunicator(application, 'ws://test/planning_poker/{}/'.format(poker_session.id))
        connected, subprotocol = await communicator.connect()
        assert connected
        if has_active_story:
            response = await communicator.receive_json_from()
            expected_response = {
                'type': 'send_json',
                'event': 'story_changed',
                'data': {
                    'id': story.id,
                    'story_label': str(story),
                    'description': story.description,
                    'votes': {}
                }
            }
            assert response == expected_response
        response = await communicator.receive_json_from()
        expected_response = {
            'type': 'send_json',
            'event': 'participants_changed',
            'data': {
                'participants': [],
            },
        }
        assert response == expected_response
        assert communicator.receive_nothing(1)
        await communicator.disconnect()

    @pytest.mark.parametrize('user_has_permission', [True, False])
    def test_receive_json(self, user_has_permission, poker_consumer, permission):
        if user_has_permission:
            poker_consumer.scope['user'].user_permissions.add(permission)

        mock_method = Mock()
        data = {'foo': 1, 'bar': 2}
        poker_consumer.commands = {
            'event': {'method': mock_method, 'required_permission': 'planning_poker.poker_permission'}}

        poker_consumer.receive_json({'event': 'event', 'data': data})
        if user_has_permission:
            mock_method.assert_called_with(**data)
        else:
            mock_method.assert_not_called()

    @patch('planning_poker.consumers.async_to_sync')
    @pytest.mark.parametrize('send_to_group', [True, False])
    def test_send_event(self, mock_async_to_sync, send_to_group, poker_consumer):
        mock_async_to_sync.side_effect = lambda args: args

        mock_group_send = Mock()
        mock_send = Mock()

        class ChannelLayer:
            group_send = mock_group_send
            send = mock_send

        poker_consumer.channel_layer = ChannelLayer()

        data = {'foo': 1, 'bar': 2}
        expected_kwargs = {'event': 'event', 'type': 'send_json', 'data': data}

        poker_consumer.room_group_name = 'group_room'
        poker_consumer.channel_name = 'channel'

        poker_consumer.send_event('event', send_to_group=send_to_group, **data)
        if send_to_group:
            mock_group_send.assert_called_with('group_room', expected_kwargs)
            mock_send.assert_not_called()
        else:
            mock_send.assert_called_with('channel', expected_kwargs)
            mock_group_send.assert_not_called()

    @pytest.mark.django_db
    @pytest.mark.parametrize('skipping_stories', [True, False])
    @pytest.mark.parametrize('has_active_story', [True, False])
    @pytest.mark.parametrize('unpokered_stories_left', [True, False])
    def test_next_story_requested(self, skipping_stories, has_active_story, unpokered_stories_left, poker_consumer,
                                  story):
        poker_consumer.poker_session.stories.create(ticket_number='FIAE-92', title='planning_poker app tests',
                                                    story_points=1)
        story_id = None
        if skipping_stories:
            new_story = poker_consumer.poker_session.stories.create(
                ticket_number='skipped',
                title='story',
                story_points=None
            )
            story_id = new_story.id
        elif unpokered_stories_left:
            new_story = poker_consumer.poker_session.stories.create(
                ticket_number='unpokered',
                title='story',
                story_points=None
            )
        if has_active_story:
            poker_consumer.poker_session.active_story = story

        mock_end_poker_session = Mock()
        mock_send_active_story_information = Mock()

        with patch.multiple(
                poker_consumer,
                end_poker_session=mock_end_poker_session,
                send_active_story_information=mock_send_active_story_information
        ):
            poker_consumer.next_story_requested(story_id=story_id)

        if unpokered_stories_left or skipping_stories:
            mock_send_active_story_information.assert_called()
            assert poker_consumer.poker_session.active_story.id == new_story.id
        else:
            mock_end_poker_session.assert_called()

    @pytest.mark.django_db
    def test_reset_requested(self, poker_consumer, story):
        poker_consumer.poker_session.active_story = story
        story.votes.create(user=poker_consumer.scope['user'], choice='1')
        assert poker_consumer.poker_session.active_story.votes.all().count() == 1

        mock_send_active_story_information = Mock()
        with patch.object(poker_consumer, 'send_active_story_information', mock_send_active_story_information):
            poker_consumer.reset_requested()

        assert poker_consumer.poker_session.active_story.votes.all().count() == 0
        mock_send_active_story_information.assert_called()

    @pytest.mark.django_db
    @pytest.mark.parametrize('has_active_story', [True, False])
    def test_set_story_points(self, poker_consumer, story, has_active_story, caplog):
        story.story_points = None
        if has_active_story:
            poker_consumer.poker_session.active_story = story

        mock_send_event = Mock()
        with patch.object(poker_consumer, 'send_event', mock_send_event):
            poker_consumer.set_story_points(3)

        if has_active_story:
            assert poker_consumer.poker_session.active_story.story_points == 3
            mock_send_event.assert_called()
        else:
            assert 'username tried to set story points with no active story.' in caplog.messages
            assert story.story_points is None
            mock_send_event.assert_not_called()

    @pytest.mark.django_db
    @pytest.mark.parametrize('has_active_story', [True, False])
    def test_vote_submitted(self, poker_consumer, story, has_active_story, caplog):
        user = poker_consumer.scope['user']
        if has_active_story:
            poker_consumer.poker_session.active_story = story
            poker_consumer.poker_session.save()

        mock_send_active_story_information = Mock()
        with patch.object(poker_consumer, 'send_active_story_information', mock_send_active_story_information):
            poker_consumer.vote_submitted('2')

        if has_active_story:
            assert story.votes.filter(user=user, choice='2').exists()
            mock_send_active_story_information.assert_called_with()
        else:
            assert 'username tried to vote with no active story.' in caplog.messages
            assert not story.votes.filter(user=user).exists()
            mock_send_active_story_information.assert_not_called()

    @pytest.mark.django_db
    @pytest.mark.parametrize('sent_to_group', [True, False])
    def test_send_active_story_information(self, sent_to_group, poker_consumer, story):
        user = poker_consumer.scope['user']
        story.story_points = None
        story.votes.create(user=user, choice='1')
        story.save()
        poker_consumer.poker_session.active_story = story

        mock_send_event = Mock()
        with patch.object(poker_consumer, 'send_event', mock_send_event):
            poker_consumer.send_active_story_information(send_to_group=sent_to_group)

        mock_send_event.assert_called_with(
            'story_changed',
            send_to_group=sent_to_group,
            id=story.id,
            story_label=str(story),
            description='description',
            votes=story.get_votes_with_voter_information()
        )

    @pytest.mark.django_db
    def test_end_poker_session(self, poker_consumer, story):
        poker_consumer.poker_session.active_story = story

        assert poker_consumer.poker_session.active_story is not None

        mock_send_event = Mock()
        with patch.object(poker_consumer, 'send_event', mock_send_event):
            poker_consumer.end_poker_session()

        assert poker_consumer.poker_session.active_story is None
        mock_send_event.assert_called_with('poker_session_ended', send_to_group=True,
                                           poker_session_end_redirect_url='/poker/')

    @pytest.mark.django_db
    def test_participants_changed(self, poker_consumer):
        participants = ['Eric', 'Kyle']
        mock_send_event = Mock()
        with patch.object(poker_consumer, 'send_event', mock_send_event):
            poker_consumer.participants_changed({'data': {'participants': participants}})

        mock_send_event.assert_called_with('participants_changed', participants=participants)

    @patch('planning_poker.consumers.Presence.objects.touch')
    def test_heartbeat_received(self, mock_touch, poker_consumer):
        poker_consumer.heartbeat_received()
        mock_touch.assert_called()
