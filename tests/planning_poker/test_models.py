from collections import OrderedDict

from django.contrib.auth import get_user_model
import pytest

from planning_poker.constants import ALL_VOTING_OPTIONS
from planning_poker.models import PokerSession, Story, Vote


@pytest.mark.django_db
class TestPokerSession:
    @pytest.mark.parametrize('name', ['', 'sprint #1', '*' * 256])
    def test_str(self, name):
        poker_session = PokerSession(poker_date='2000-01-01', name=name)
        assert str(poker_session) == name


@pytest.mark.django_db
class TestStory:
    @pytest.mark.parametrize('ticket_number', ['TEST', '*' * 256])
    @pytest.mark.parametrize('title', ['test story', '~' * 256, None])
    def test_str(self, ticket_number, title):
        story = Story(ticket_number=ticket_number, title=title)
        result = str(story)
        if title:
            assert result == '{}: {}'.format(ticket_number, title)
        else:
            assert result == ticket_number

    def test_get_votes_with_voter_information(self, story):
        users = [get_user_model().objects.create(username='user{}'.format(i), password='password') for i in range(1, 4)]
        story.votes.create(user=users[0], choice='2')
        story.votes.create(user=users[1], choice='2')
        story.votes.create(user=users[2], choice='1')

        expected_result = OrderedDict([
            ('2', [{'id': users[0].id, 'name': users[0].username}, {'id': users[1].id, 'name': users[1].username}]),
            ('1', [{'id': users[2].id, 'name': users[2].username}])
        ])

        assert story.get_votes_with_voter_information() == expected_result


@pytest.mark.django_db
class TestVote:
    @pytest.mark.parametrize('choice, choice_display, username', [
        (ALL_VOTING_OPTIONS[0][0], ALL_VOTING_OPTIONS[0][1], 'Bob'),
        (ALL_VOTING_OPTIONS[9][0], ALL_VOTING_OPTIONS[9][1], 'Billy'),
    ])
    def test_str(self, choice, choice_display, username, story):
        user = get_user_model().objects.create(username=username, password='password')
        vote = Vote(story=story, user=user, choice=choice)
        assert str(vote) == '{user} voted {choice} for story {story}'.format(
            user=user,
            choice=choice_display,
            story=story
        )
