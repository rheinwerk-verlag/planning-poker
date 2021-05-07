from unittest.mock import Mock, patch

from planning_poker.backends.ticket.base import BaseTicketBackend
from planning_poker.templatetags.planning_poker_filters import get_url


@patch('planning_poker.templatetags.planning_poker_filters.get_ticket_system')
def test_get_url(mock_get_ticket_system, story):

    mock_get_story_url = Mock(return_value='test url')

    class MockTicketBackend(BaseTicketBackend):
        def get_story_url(self, *args, **kwargs):
            return mock_get_story_url(*args, **kwargs)

    mock_get_ticket_system.return_value = MockTicketBackend()

    assert get_url(story) == 'test url'
    mock_get_story_url.assert_called_with(story)
