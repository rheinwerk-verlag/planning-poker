Planning Poker
================================

The idea for the Planning Poker app came to life during the 2020 Covid pandemic with the aim to provide agile teams with
an easy way to perform their planning poker sessions from the safety of their homes. It was developed with flexibility
and extensibility in mind. Powered by a Django backend and Vue frontend.

Features
========
* 🔍 This app comes with an **easy to use interface** and provides all the necessary data for estimating the scope of your stories on a single page.

* 🧑‍💻 The users are separated into **voters** and **moderators** who see and do different things during a session. See `roles` for more information

* 👥 See who participates in your session via a **live updated list of users**.

* 🌙 Native **dark mode**


Quickstart
==========
Do you have Django installed? Follow these steps `here <https://docs.djangoproject.com/en/3.2/topics/install/>`_ if you
haven't.

Basic understanding of Python and Django is not required but definitely recommended before you start installing this
application.

* Have an existing project where you want to include the Planning Poker app or create a new one. ::

    $ django-admin startproject planning-poker-site

* Install the app via pip. ::

    $ pip install planning-poker

* Configure your settings. They are located in `planning-poker-site/settings.py` if you chose to setup a new project. Youl'll find the minimal settings required for the Planning Poker app below. See `configuration` for more ways to customize the application to fit your needs.

    .. code-block:: python

        INSTALLED_APPS = [
            ...
            'planning_poker'
        ]

        # This is not the optimal channel layer and should not be used for production.
        # See https://channels.readthedocs.io/en/stable/topics/channel_layers.html for an alternative.
        CHANNEL_LAYERS = {
            'default': {
                'BACKEND': 'channels.layers.InMemoryChannelLayer'
            }
        }

        LOGIN_URL = 'admin:login'
        LOGOUT_URL = 'admin:logout'

* Include `planning-poker`'s URLs in your urls which can be found in `planning-poker-site/urls.py` in the fresh project.

.. code-block:: python

    from django.urls import include, path

    urlpatterns = [
        # The first entry isn't needed but nice to have if the sole purpose of this project is serving the Planning Poker app.
        path('', RedirectView.as_view(pattern_name='planning_poker:index'), name='redirect_to_poker_index'),
        path('poker/', include('planning_poker.urls')),
    ]

* Run the migrations. ::

    $ python manage.py migrate

* You can now start your server. ::

    $ python manage.py runserver 0.0.0.0:8000

See the user `docs` for more information on how to use the Planning Poker app.
