from django.utils.translation import ugettext_lazy as _

FIBONACCI_CHOICES = [
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('5', '5'),
    ('8', '8'),
    ('13', '13'),
    ('21', '21'),
    ('34', '34'),
]

TOO_LARGE = 'Too large'
NO_IDEA = 'No idea'

NON_POINT_OPTIONS = [
    (TOO_LARGE, _('Too large')),
    (NO_IDEA, _('No idea'))
]

ALL_VOTING_OPTIONS = FIBONACCI_CHOICES + NON_POINT_OPTIONS
