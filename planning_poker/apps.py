from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PlanningPokerConfig(AppConfig):
    name = 'planning_poker'
    verbose_name = _('Planning Poker')

    def ready(self):
        from . import receivers  # noqa
