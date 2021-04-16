from unittest.mock import Mock, patch

import pytest
from channels_presence.models import Room, Presence
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from planning_poker.receivers import broadcast_presence


@patch('planning_poker.receivers.async_to_sync')
@pytest.mark.django_db
def test_broadcast_presence(mock_async_to_sync):
    mock_group_send = Mock()
    mock_async_to_sync.return_value = mock_group_send

    model = get_user_model()
    room = Room.objects.create(channel_name='test room')
    moderate_permission = Permission.objects.get(codename='moderate')
    vote_permission = Permission.objects.get(codename='vote')

    users = [
        {'username': 'superuser', 'permissions': [moderate_permission, vote_permission]},
        {'username': 'voter', 'permissions': [vote_permission]},
        {'username': 'moderator', 'permissions': [moderate_permission]},
        {'username': 'spectator', 'permissions': []}
    ]

    for user in users:
        username = user['username']
        created_user = model.objects.create(username=username, password=username)
        for permission in user['permissions']:
            created_user.user_permissions.add(permission)
        Presence.objects.create(channel_name='{} channel'.format(username), room=room, user=created_user)

    with patch('planning_poker.receivers.channel_layer'):
        broadcast_presence(room)

    expected_message = {
        'type': 'participants.changed',
        'data': {
            'participants': [
                {
                    'id': 3,
                    'username': 'moderator',
                    'permissions': ['planning_poker.moderate']
                },
                {
                    'id': 4,
                    'username': 'spectator',
                    'permissions': []
                },
                {
                    'id': 1,
                    'username': 'superuser',
                    'permissions': ['planning_poker.moderate', 'planning_poker.vote']
                },
                {
                    'id': 2,
                    'username': 'voter',
                    'permissions': ['planning_poker.vote']
                },
            ]
        }
    }
    mock_group_send.assert_called_with('test room', expected_message)
