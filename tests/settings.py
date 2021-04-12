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
    'planning_poker',
)

ROOT_URLCONF = 'planning_poker.urls'

SITE_ID = 1
