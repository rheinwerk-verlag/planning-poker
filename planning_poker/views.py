from typing import Any, Dict

from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db.models import Count, Q
from django.shortcuts import resolve_url
from django.views.generic import ListView, DetailView

from .constants import FIBONACCI_CHOICES, NON_POINT_OPTIONS
from .models import PokerSession


class LoginLogoutMixin(LoginRequiredMixin):
    logout_url = None

    def get_logout_url(self) -> str:
        """
        Override this method to override the logout_url attribute.
        """
        logout_url = self.logout_url or getattr(settings, 'LOGOUT_URL', None)
        if not logout_url:
            raise ImproperlyConfigured(
                '{0} is missing the logout_url attribute. Define {0}.logout_url, settings.LOGOUT_URL, or override '
                '{0}.get_logout_url().'.format(self.__class__.__name__)
            )
        return resolve_url(logout_url)

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['logout_url'] = self.get_logout_url()
        return context


class PokerSessionView(LoginLogoutMixin, DetailView):
    model = PokerSession
    template_name = 'planning_poker/poker_session.html'

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['options'] = {
            'point_options': [list(choice) for choice in FIBONACCI_CHOICES],
            'non_point_options': [list(choice) for choice in NON_POINT_OPTIONS]
        }
        context['stories'] = [
            {
                'id': story.id,
                'title': str(story),
                'points': str(story.story_points) if story.story_points else None
            } for story in self.object.stories.all()
        ]
        context['permissions'] = {
            'vote': self.request.user.has_perm('planning_poker.vote'),
            'moderate': self.request.user.has_perm('planning_poker.moderate')
        }
        context['poker_session_end_redirect_url'] = getattr(settings, 'POKER_SESSION_END_REDIRECT_URL',
                                                            resolve_url('planning_poker:index'))
        return context


class IndexView(LoginLogoutMixin, ListView):
    queryset = PokerSession.objects.filter(stories__story_points__isnull=True).distinct().annotate(
        unpokered_stories=Count('id', filter=Q(stories__story_points__isnull=True))
    )
    template_name = 'planning_poker/index.html'
