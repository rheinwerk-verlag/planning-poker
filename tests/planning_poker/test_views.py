from django.contrib.auth.models import Permission
from django.core.exceptions import ImproperlyConfigured
from django.views.generic import TemplateView
import pytest

from planning_poker.constants import FIBONACCI_CHOICES, NON_POINT_OPTIONS
from planning_poker.views import LoginLogoutMixin


class TestLoginLogoutMixin:
    @pytest.mark.parametrize('settings_logout_url', [None, '/settings/logout/'])
    @pytest.mark.parametrize('view_logout_url', [None, '/view/logout/'])
    def test_get_logout_url(self, view_logout_url, settings_logout_url, settings):
        settings.LOGOUT_URL = settings_logout_url
        view = LoginLogoutMixin()
        view.logout_url = view_logout_url
        if not (view_logout_url or settings_logout_url):
            with pytest.raises(ImproperlyConfigured):
                view.get_logout_url()
        else:
            assert view.get_logout_url() == view_logout_url or settings_logout_url

    def test_get_context_data(self):
        class MockView(LoginLogoutMixin, TemplateView):
            def get_context_data(self, **kwargs):
                return super().get_context_data(**kwargs)

        view = MockView()
        view.logout_url = '/view/logout'
        context = view.get_context_data()
        assert context['logout_url'] == '/view/logout'


class TestPokerSessionView:
    @pytest.mark.django_db
    @pytest.mark.parametrize('has_moderate_permission', [True, False])
    @pytest.mark.parametrize('has_vote_permission', [True, False])
    def test_get_context_data(self, client, django_user_model, has_vote_permission, has_moderate_permission,
                              poker_session, story):
        user = django_user_model.objects.create(username='test user', password='super-secret')
        if has_vote_permission:
            user.user_permissions.add(Permission.objects.get(codename='vote'))
        if has_moderate_permission:
            user.user_permissions.add(Permission.objects.get(codename='moderate'))
        client.force_login(user)

        response = client.get('/poker/{}/'.format(poker_session.id), follow=True)

        expected_options = {
            'point_options': [list(choice) for choice in FIBONACCI_CHOICES],
            'non_point_options': [list(choice) for choice in NON_POINT_OPTIONS]
        }
        assert response.context['options'] == expected_options

        expected_stories = [
            {'id': story.id, 'title': str(story), 'points': str(story.story_points)}
        ]
        assert response.context['stories'] == expected_stories

        expected_permissions = {
            'vote': has_vote_permission,
            'moderate': has_moderate_permission
        }
        assert response.context['permissions'] == expected_permissions
