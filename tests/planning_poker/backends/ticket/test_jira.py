from unittest.mock import Mock, patch

import pytest
from django.test import override_settings
from jira import JIRAError

from planning_poker.backends.ticket.jira import JiraTicketBackend


class JiraFields:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            self.__setattr__(key, value)


class JiraTestStory:
    def __init__(self, fields, rendered_fields, **kwargs):
        for key, value in kwargs.items():
            self.__setattr__(key, value)
        self.fields = JiraFields(**fields)
        self.renderedFields = JiraFields(**rendered_fields)


class TestJiraTicketBackend:
    test_settings = {
        'BACKEND': 'test.backend',
        'API_URL': 'http://test_url',
        'USERNAME': 'username',
        'PASSWORD': 'password',
        'STORY_POINTS_FIELD': 'customfield_1337'
    }

    @override_settings(TICKET_SYSTEM=test_settings)
    def test_init_no_kwargs(self):
        backend = JiraTicketBackend()
        assert backend.api_url == 'http://test_url'
        assert backend.username == 'username'
        assert backend.password == 'password'
        assert backend.story_points_field == 'customfield_1337'

    @override_settings(TICKET_SYSTEM=test_settings)
    def test_init_kwargs(self):
        kwargs = {
            'api_url': 'http://different_url',
            'username': 'different username',
            'password': 'different password',
            'story_points_field': 'customfield_not_1337'
        }
        backend = JiraTicketBackend(**kwargs)
        assert backend.api_url == kwargs['api_url']
        assert backend.username == kwargs['username']
        assert backend.password == kwargs['password']
        assert backend.story_points_field == kwargs['story_points_field']

    @patch('planning_poker.backends.ticket.jira.JIRA')
    def test_client(self, mock_jira, jira_ticket_backend):
        mock_jira.return_value = 'jira client'

        assert jira_ticket_backend.client == 'jira client'
        mock_jira.assert_called_with('http://test_url', basic_auth=('username', 'password'))

    @patch('planning_poker.backends.ticket.jira.JIRA')
    @pytest.mark.parametrize('jira_error, side_effect', [
        (True, JIRAError()),
        (False, [[
            JiraTestStory(fields={'summary': 'write tests'}, rendered_fields={'description': 'foo'}, key='FIAE-1'),
            JiraTestStory(fields={'summary': 'more tests'}, rendered_fields={'description': 'bar'}, key='FIAE-2')
        ]])
    ]
    )
    def test_get_poker_stories(self, mock_jira, jira_error, side_effect, jira_ticket_backend):
        mock_client = Mock()
        mock_jira.return_value = mock_client
        mock_client.search_issues.side_effect = side_effect
        expected_result = [] if jira_error else [
            {'number': 'FIAE-1', 'title': 'write tests', 'description': 'foo'},
            {'number': 'FIAE-2', 'title': 'more tests', 'description': 'bar'}
        ]

        assert jira_ticket_backend.get_poker_stories(search_string='project=FIAE') == expected_result
        mock_client.search_issues.assert_called_with(
            jql_str='project=FIAE',
            expand='renderedFields',
            fields=['summary', 'description']
        )

    def test_get_story_url(self, jira_ticket_backend, story):
        assert jira_ticket_backend.get_story_url(story) == 'http://test_url/browse/' + story.ticket_number

    @pytest.mark.django_db
    @patch('planning_poker.backends.ticket.jira.JIRA')
    def test_set_story_points(self, mock_jira, jira_ticket_backend, story):
        story.story_points = 3
        story.save()

        mock_story = Mock()
        mock_client = Mock()
        mock_client.issue.return_value = mock_story
        mock_jira.return_value = mock_client

        jira_ticket_backend.set_story_points(story)

        mock_client.issue.assert_called_with(id=story.ticket_number, fields='')
        mock_story.update.assert_called_with(fields={'customfield_1337': 3})
