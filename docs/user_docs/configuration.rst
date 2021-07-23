Configuration
=============
The Planning Poker app provides a few options you can set in your settings to customize your experience.

Required Settings
-----------------

- ``CHANNEL_LAYERS``: ``django_channels`` requires a channel layer to be configured. See
  `their docs <https://channels.readthedocs.io/en/stable/topics/channel_layers.html>`_ for more information on how to
  setup a channel layer.

- ``LOGIN_URL``: This URL will be used to redirect users after a successful login attempt and is required for the
  navbar.

- ``LOGOUT_URL``: This URL will be used to redirect users after logging out and is also required for the navbar.


Optional Settings
-----------------

- ``POKER_SESSION_END_REDIRECT_URL`` - default ``'planning_poker:index'``: This URL will be used to redirect users when
  the last story of a poker session has been pokered and the points are set by a moderator. The value can be anything
  URL-like, e.g. a hardcoded string ``'https://rheinwerk-verlag.de'`` or a view name (like the default value).
