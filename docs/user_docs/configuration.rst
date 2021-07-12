Configuration
=============
The Planning Poker app provides a few options you can set in your settings to customize your experience.

Required Settings
-----------------

- :code:`CHANNEL_LAYERS`: :code:`django_channels` requires a channel layer to be configured. See
  `their docs <https://channels.readthedocs.io/en/stable/topics/channel_layers.html>`_ for more information on how to
  setup a channel layer.

- :code:`LOGIN_URL`: This URL will be used to redirect users after a successful login attempt and is required for the
  navbar.

- :code:`LOGOUT_URL`: This URL will be used to redirect users after a successful logout attempt and is also required
  for the navbar.


Optional Settings
-----------------

- :code:`POKER_SESSION_END_REDIRECT_URL` - default :code:`'planning_poker:index'`: This URL will be used to redirect
  users when the last story of a poker session has been pokered and the points are set by a moderator. The value can be
  anything URL-like e.g. a hardcoded string :code:`'https://rheinwerk-verlag.de'`, a view name (like the default value),
  or the return value of Django's :code:`reverse()`.

  .. note::
     If you don't want to change the default value of the :code:`POKER_SESSION_END_REDIRECT_URL` setting, make sure that
     :code:`'planning_poker:index'` is a valid view name for your project by including :code:`planning_poker.urls` in your
     :code:`urls.py`
