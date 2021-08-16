from collections import defaultdict, OrderedDict
from typing import Dict, List
try:
    # The OrderedDict was added to the typing module in Python version 3.7.
    # Fall back to the default Dict type in order to provide backwards compatibility for Python 3.6.
    from typing import OrderedDict as OrderedDictType
except ImportError:  #  pragma: no cover
    OrderedDictType = Dict

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from .constants import FIBONACCI_CHOICES, ALL_VOTING_OPTIONS


class PokerSession(models.Model):
    #: The date on which the poker session should take place.
    poker_date = models.DateField(verbose_name=_('Poker Date'))
    #: The poker session's name. Used for displaying it to the user.
    name = models.CharField(max_length=200, verbose_name=_('Name'))
    #: The story which is currently active in this poker session.
    active_story = models.OneToOneField(
        'Story',
        on_delete=models.SET_NULL,
        verbose_name=_('Active Story'),
        related_name='active_in',
        null=True
    )

    class Meta:
        ordering = ['-poker_date']
        verbose_name = _('Poker Session')
        verbose_name_plural = _('Poker Sessions')

    def __str__(self) -> str:
        return self.name


class Story(models.Model):
    #: The story's ticket number. Used for displaying the story to the user.
    ticket_number = models.CharField(max_length=200, verbose_name=_('Ticket Number'))
    #: The story's title. Used for displaying the story to the user.
    title = models.CharField(max_length=200, verbose_name=_('Title'), blank=True)
    #: The story's description. This is the main source of information for participants in a poker session.
    description = models.TextField(verbose_name=_('Description'), blank=True)
    #: The estimated story points. The value is either an element of
    #: :py:data:`planning_poker.constants.FIBONACCI_CHOICES` or ``None``.
    story_points = models.PositiveSmallIntegerField(
        verbose_name=_('Story Points'),
        help_text=_('The amount of points this story takes up in the sprint'),
        null=True,
        blank=True,
        choices=[(None, '-')] + [(int(number), label) for number, label in FIBONACCI_CHOICES]
    )
    #: The poker session to which this story belongs to.
    poker_session = models.ForeignKey(
        PokerSession, on_delete=models.SET_NULL,
        verbose_name=_('Poker Session'),
        related_name='stories',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = _('Story')
        verbose_name_plural = _('Stories')
        order_with_respect_to = 'poker_session'
        permissions = [
            ('vote', 'Can vote for a story.'),
            ('moderate', 'Is able to moderate a planning_poker session.'),
        ]

    def __str__(self) -> str:
        if self.title:
            return '{}: {}'.format(self.ticket_number, self.title)
        return self.ticket_number

    def get_votes_with_voter_information(self) -> OrderedDictType[str, List[Dict[str, str]]]:
        """Return a sorted list with each choice + the users who voted for that choice.

        :return: A sorted list with each choice + the users who voted for that choice.
        """
        votes = defaultdict(list)
        for vote in self.votes.select_related('user'):
            votes[vote.choice].append({'id': vote.user.id, 'name': vote.user.username})
        return OrderedDict(sorted(votes.items(), key=lambda vote: len(vote[1]), reverse=True))


class Vote(models.Model):
    #: The story for which this vote was casted for.
    story = models.ForeignKey(
        Story,
        on_delete=models.CASCADE,
        verbose_name=_('Story'),
        related_name='votes'
    )
    #: The user who casted the vote.
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('User'),
        related_name='votes'
    )
    #: The option which was voted for. See :py:data:`planning_poker.constants.ALL_VOTING_OPTIONS` for all possible
    #: values.
    choice = models.CharField(
        max_length=200,
        verbose_name=_('Choice'),
        choices=ALL_VOTING_OPTIONS
    )

    class Meta:
        verbose_name = _('Vote')
        verbose_name_plural = _('Votes')
        constraints = [
            models.UniqueConstraint(fields=['story', 'user'], name='A user can only vote once for each story.')
        ]

    def __str__(self) -> str:
        return _('{user} voted {choice} for story {story}').format(
            user=self.user,
            choice=self.get_choice_display(),
            story=self.story
        )
