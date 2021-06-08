from typing import Any, Callable

from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.db.models import QuerySet
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _

from .models import PokerSession, Story, Vote


class DropdownFilter(admin.filters.RelatedFieldListFilter):
    template = 'admin/dropdown_filter.html'


class StoryInline(admin.TabularInline):
    model = Story
    readonly_fields = ('story_points',)
    extra = 1


class VoteInline(admin.TabularInline):
    can_delete = False
    extra = 0
    model = Vote
    readonly_fields = ('user', 'choice')

    def has_add_permission(self, *args, **kwargs):
        return False


@admin.register(PokerSession)
class PokerSessionAdmin(admin.ModelAdmin):
    date_hierarchy = 'poker_date'
    fields = ['name', 'poker_date']
    inlines = [StoryInline]
    list_display = ('__str__', 'poker_date')
    list_filter = ['poker_date']
    search_fields = ['name']


@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    readonly_fields = ('story_points',)
    fieldsets = [
        (None, {'fields': ['ticket_number', 'title', 'description']}),
        (_('Poker Data'), {'fields': ['poker_session', 'story_points']}),
    ]
    inlines = [VoteInline]
    list_display = ('__str__', 'story_points', 'poker_session')
    list_filter = [('poker_session', DropdownFilter), 'story_points']
    search_fields = ['ticket_number', 'title', 'poker_session__name']

    @classmethod
    def add_action(cls, action: Callable[[ModelAdmin, HttpRequest, QuerySet], Any], label: str):
        """Add the given action to the list of admin actions.
        This could be used by extensions to add story based actions.

        :param Callable[[ModelAdmin, HttpRequest, QuerySet], Any] action: The action which should be added to the list.
        :param str label: The human readable label which should be used to display the action in the list of actions.
        """
        action.short_description = label
        cls.actions = [*cls.actions, action]
