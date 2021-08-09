# -*- coding: utf-8 -*-

# CHANGE THIS!
SECRET_KEY = '96a40240ed25433cb8ff8ce819bf710b'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'planning_poker.db',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'channels',
    'planning_poker.apps.ChannelsPresenceConfig',
    'planning_poker.apps.PlanningPokerConfig',
)

ROOT_URLCONF = 'planning_poker.urls'

WSGI_APPLICATION = 'example.wsgi.application'
ASGI_APPLICATION = 'example.routing.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer'
    },
}

POKER_SESSION_END_REDIRECT_URL = 'index'
