from django.contrib.admin import site
import pytest

from planning_poker.admin import StoryAdmin, VoteInline
from planning_poker.models import Story, Vote


class TestStoryAdmin:
    @pytest.mark.parametrize('label', ('', 'test label'))
    def test_add_action(self, label):
        def dummy_action():
            pass
        dummy_action.short_description = 'dummy action'

        StoryAdmin.add_action(dummy_action, label)
        assert dummy_action.short_description == label or 'dummy action'
        assert dummy_action in StoryAdmin.actions


class TestVoteInline:
    def test_has_add_permission(self):
        site.register(Vote, VoteInline)
        vote_inline = VoteInline(Story, site)
        assert not vote_inline.has_add_permission()
