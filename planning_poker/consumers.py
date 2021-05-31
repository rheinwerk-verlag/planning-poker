import logging
from typing import Dict

from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer
from channels_presence.models import Presence, Room
from django.utils.functional import cached_property

from .models import Story, PokerSession

MODERATE_PERMISSION = '.'.join((Story._meta.app_label, 'moderate'))
VOTE_PERMISSION = '.'.join((Story._meta.app_label, 'vote'))

logger = logging.getLogger(__name__)


class PokerConsumer(JsonWebsocketConsumer):
    """Consumer responsible for the communication between the moderator's and voter's websockets."""

    def __init__(self, *args, **kwargs):
        """Initialize a PokerConsumer and set the dict of callable commands."""
        super().__init__(*args, **kwargs)
        self.commands = {
            'reset_requested': {'method': self.reset_requested, 'required_permission': MODERATE_PERMISSION},
            'next_story_requested': {'method': self.next_story_requested, 'required_permission': MODERATE_PERMISSION},
            'points_submitted': {'method': self.set_story_points, 'required_permission': MODERATE_PERMISSION},
            'vote_submitted': {'method': self.vote_submitted, 'required_permission': VOTE_PERMISSION},
            'heartbeat': {'method': self.heartbeat_received, 'required_permission': None}
        }

    @cached_property
    def poker_session(self) -> PokerSession:
        """Return the planning_poker session corresponding to the websocket's url.

        :return: The planning_poker session corresponding to the websocket's url.
        :rtype: planning_poker.models.PokerSession
        """
        return PokerSession.objects.select_related('active_story').get(
            pk=self.scope['url_route']['kwargs']['poker_session']
        )

    def connect(self) -> None:
        """Accept the connection from a websocket."""

        self.room_group_name = 'poker_session_{}'.format(self.poker_session.id)

        Room.objects.add(self.room_group_name, self.channel_name, self.scope['user'])

        self.accept()
        if self.poker_session.active_story:
            self.send_active_story_information(send_to_group=False)

    def disconnect(self, **kwargs) -> None:
        """Remove self from the current group."""
        Room.objects.remove(self.room_group_name, self.channel_name)

    def receive_json(self, content: Dict, **kwargs) -> None:
        """Call the given method with its arguments.
        A log entry is made and no method is executed, if the user doesn't have the required permission.

        :param dict content: A dict containing the command and additional arguments.
                             For example: '{'event': 'foo', 'data': data}'
        :param kwargs: Additional keyword arguments.
        """
        user = self.scope['user']
        command = self.commands[content.pop('event')]
        required_permission = command['required_permission']
        if required_permission is None or user.has_perm(required_permission):
            command['method'](**content['data'])
        else:
            logger.warning(
                '%(user)s tried to execute %(method)s without the required permission: %(required_permission)s',
                {'user': user, **command}
            )

    def send_event(self, event: str, send_to_group: bool = True, **data: Dict) -> None:
        """Send an event with the given data either to the channel or to the whole group.

        :param str event: The name of the event which should be sent.
        :param bool send_to_group: Flag whether the event should be sent to the whole group or not. Default True.
        :param dict data: The data which should be sent along the event.
        """
        if send_to_group:
            send_method = self.channel_layer.group_send
            channel_name = self.room_group_name
        else:
            send_method = self.channel_layer.send
            channel_name = self.channel_name
        async_to_sync(send_method)(
            channel_name,
            {
                'type': 'send_json',
                'event': event,
                'data': data
            }
        )

    def next_story_requested(self, story_id: int = None) -> None:
        """Set the planning_poker session's active story and send all necessary data to the websockets.

        :param int story_id: The id of the story which should become the active story.
        """
        self.poker_session.refresh_from_db()
        if story_id is None:
            active_story_order = self.poker_session.active_story._order if self.poker_session.active_story else -1
            new_active_story = self.poker_session.stories.filter(
                story_points__isnull=True,
                _order__gt=active_story_order
            ).first()
        else:
            new_active_story = self.poker_session.stories.get(pk=story_id)
        if new_active_story is None:
            self.end_poker_session()
        else:
            self.poker_session.active_story = new_active_story
            self.poker_session.save()
            self.send_active_story_information()

    def reset_requested(self) -> None:
        """Remove all votes from the currently active story."""
        self.poker_session.active_story.votes.all().delete()
        self.send_active_story_information()

    def set_story_points(self, story_points: int) -> None:
        """Set the story's story points in the database.

        :param int story_points: The points which the story should have.
        """
        active_story = self.poker_session.active_story
        if active_story is None:
            logger.warning('%(user)s tried to set story points with no active story.', {'user': self.scope['user']})
            return
        active_story.story_points = story_points
        active_story.save()
        self.send_event('story_points_submitted', story_points=story_points)

    def vote_submitted(self, choice: str) -> None:
        """Dispatch an event containing the user and their choice + the same information in a signed string.

        :param str choice: The choice for the story's points the user made.
        """
        self.poker_session.refresh_from_db()
        active_story = self.poker_session.active_story
        user = self.scope['user']
        if active_story is None:
            logger.warning('%(user)s tried to vote with no active story.', {'user': user})
            return
        active_story.votes.update_or_create(user=user, defaults={'choice': choice})
        self.send_active_story_information()

    def send_active_story_information(self, send_to_group: bool = True) -> None:
        """Dispatch an Event containing the story's information.

        :param bool send_to_group: Flag whether the event should be sent to the whole group or not. Default True.
        """
        self.send_event(
            'story_changed',
            send_to_group=send_to_group,
            id=self.poker_session.active_story.id,
            story_label=str(self.poker_session.active_story),
            description=self.poker_session.active_story.description,
            votes=self.poker_session.active_story.get_votes_with_voter_information()
        )

    def end_poker_session(self) -> None:
        """Dispatch an Event which ends the planning_poker session."""
        self.poker_session.active_story = None
        self.poker_session.save()
        self.send_event(
            'poker_session_ended',
            send_to_group=True
        )

    def heartbeat_received(self) -> None:
        """Update the 'last seen' timestamp."""
        Presence.objects.touch(self.channel_name)

    def participants_changed(self, message: Dict) -> None:
        """Dispatch an event containing a list of all participants.

        :param dict message: The message contains information about the planning_poker session's active participants.
        """
        self.send_event('participants_changed', **message['data'])
