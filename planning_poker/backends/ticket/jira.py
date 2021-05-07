import logging
from urllib.parse import urljoin

from django.conf import settings
from django.utils.functional import cached_property
from jira import JIRA, JIRAError

from .base import BaseTicketBackend

logger = logging.getLogger(__name__)


class JiraTicketBackend(BaseTicketBackend):
    def __init__(self, api_url=None, username=None, password=None, story_points_field=None, **kwargs):
        """Note that you need the jira specific STORYPOINTS_FIELD setting in your backend settings, since the exact
        field differs from backend to backend. e.g. customfield__10003"""
        super().__init__()
        self.api_url = api_url or settings.TICKET_SYSTEM['API_URL']
        self.username = username or settings.TICKET_SYSTEM['USERNAME']
        self.password = password or settings.TICKET_SYSTEM['PASSWORD']
        self.story_points_field = story_points_field or settings.TICKET_SYSTEM['STORY_POINTS_FIELD']

    @cached_property
    def client(self):
        return JIRA(self.api_url, basic_auth=(self.username, self.password))

    def set_story_points(self, story, *args, **kwargs):
        jira_story = self.client.issue(id=story.ticket_number, fields='')
        jira_story.update(fields={self.story_points_field: story.story_points})

    def get_poker_stories(self, *args, **kwargs):
        results = []
        try:
            results = self.client.search_issues(
                jql_str=kwargs['search_string'],
                expand='renderedFields',
                fields=['summary', 'description']
            )
        except JIRAError as e:
            logger.warning(e)
        else:
            results = [
                {
                    'number': story.key,
                    'title': story.fields.summary,
                    'description': story.renderedFields.description
                } for story in results]
        return results

    def get_story_url(self, story):
        return urljoin(self.api_url, 'browse/' + story.ticket_number)
