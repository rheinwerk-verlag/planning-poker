from unittest.mock import Mock, patch

from django.test import override_settings

from poker.backends.ticket import get_ticket_system


@override_settings(TICKET_SYSTEM={'BACKEND': 'test.backend'})
@patch('planning_poker.backends.ticket.import_string')
def test_get_ticket_system(mock_import_string):
    parameters = {'a': 1, 'b': 2}
    mock_backend = Mock()
    mock_import_string.return_value = mock_backend

    get_ticket_system(**parameters)
    mock_import_string.assert_called_with('test.backend')
    mock_backend.assert_called_with(**parameters)
