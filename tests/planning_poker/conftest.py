import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission, ContentType
from django.core.management import call_command
from django.test import override_settings

from planning_poker.backends.ticket.jira import JiraTicketBackend
from planning_poker.consumers import PokerConsumer, TicketConsumer
from planning_poker.models import PokerSession, Story


@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command('loaddata', 'test_data.json')


@pytest.fixture
def poker_consumer(db):
    consumer = PokerConsumer(scope={
        'url_route': {'kwargs': {'poker_session': 1}},
        'user': get_user_model().objects.create(username='username', password='password')
    })
    return consumer


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
def ticket_consumer():
    return TicketConsumer(scope={})


@pytest.fixture()
@override_settings(TICKET_SYSTEM={
    'BACKEND': 'test.backend',
    'API_URL': 'http://test_url',
    'USERNAME': 'username',
    'PASSWORD': 'password',
    'STORY_POINTS_FIELD': 'customfield_1337'
})
def jira_ticket_backend():
    return JiraTicketBackend()
