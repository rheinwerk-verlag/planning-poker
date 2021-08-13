from channels_presence.apps import RoomsConfig
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PlanningPokerConfig(AppConfig):
    default = True
    default_auto_field = 'django.db.models.AutoField'
    name = 'planning_poker'
    verbose_name = _('Planning Poker')

    def ready(self):
        from . import receivers  # noqa


class ChannelsPresenceConfig(RoomsConfig):
    default_auto_field = 'django.db.models.AutoField'
    name = 'channels_presence'
    verbose_name = _('Channels Presence')
