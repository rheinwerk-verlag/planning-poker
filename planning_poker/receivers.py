from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from channels_presence.models import Room
from channels_presence.signals import presence_changed
from django.dispatch import receiver

from .consumers import MODERATE_PERMISSION, VOTE_PERMISSION

permissions = [MODERATE_PERMISSION, VOTE_PERMISSION]

channel_layer = get_channel_layer()


@receiver(presence_changed)
def broadcast_presence(room: Room, **kwargs):
    """Broadcast the new list of present users to the.

    :param room: The room from which a presence was added or removed.
    """
    participants = []
    for user in room.get_users().order_by('username'):
        participant = {
            'id': user.id,
            'username': user.username,
            'permissions': [permission for permission in permissions if user.has_perm(permission)]
        }
        participants.append(participant)

    channel_layer_message = {
        'type': 'participants.changed',
        'data': {
            'participants': participants
        }
    }

    async_to_sync(channel_layer.group_send)(room.channel_name, channel_layer_message)
