# -*- coding: utf-8 -*-

# CHANGE THIS!
SECRET_KEY = '96a40240ed25433cb8ff8ce819bf710b'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'django_wishlist.db',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}


MIDDLEWARE_CLASSES = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'wishlist.middleware.WishlistMiddleware',
]


SESSION_ENGINE = 'django.contrib.sessions.backends.cache'


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
