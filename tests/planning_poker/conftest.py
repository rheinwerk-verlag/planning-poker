from django.contrib.auth import get_user_model
from django.contrib.auth.models import ContentType, Permission
import pytest

from planning_poker.consumers import PokerConsumer
from planning_poker.models import PokerSession, Story


@pytest.fixture
def permission(db):
    return Permission.objects.create(
        name='planning_poker permission',
        content_type=ContentType.objects.get_for_model(PokerSession),
        codename='poker_permission'
    )


@pytest.fixture
def story(db):
    return Story.objects.create(ticket_number='test', title='story', story_points=1, description='description')


@pytest.fixture
def poker_session(db, story):
    poker_session = PokerSession.objects.create(poker_date='2000-01-01', name='test session')
    story.poker_session = poker_session
    story.save()
    return poker_session


@pytest.fixture
def poker_consumer(db, poker_session):
    consumer = PokerConsumer()
    consumer.scope = {
        'url_route': {'kwargs': {'poker_session': poker_session.id}},
        'user': get_user_model().objects.create(username='username', password='password')
    }
    consumer.channel_name = 'poker_session_1'
    return consumer
