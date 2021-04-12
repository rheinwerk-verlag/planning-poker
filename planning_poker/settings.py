# -*- coding: utf-8 -*

from __future__ import absolute_import, unicode_literals

from django.core.exceptions import ImproperlyConfigured


DEFAULT_SETTINGS = {}


def apply_settings():
    """Updates django.conf.settings with application settings."""
    # Don't import settings globally, so that settings loading happens lazily
    from django.conf import settings

    for key, value in DEFAULT_SETTINGS.iteritems():
        if not hasattr(settings, key):
            setattr(settings, key, value)

    # This is an example for checking the presence of a required settings
    # Replace it with code checking your own settings or remove it!
    if getattr(settings, 'PLANNING_POKER_IMPORTANT') is None:
        raise ImproperlyConfigured('Please make sure you specified a PLANNING_POKER_IMPORTANT setting.')
