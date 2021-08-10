Developer Documentation
=======================

.. toctree::
   :maxdepth: 2
   :caption: Contents

   setup
   testing
   consumers
   models
   views
   presence
   admin
   constants
   deployment

The Planning Poker app can be used and expanded like any other Django app. If you want to extend this app's
functionality, you should consider writing an extension app. Feel free and see the
`Jira extension <https://github.com/rheinwerk-verlag/planning-poker-jira>`_ for inspiration on how to design your
extension.

This project uses websockets provided by `Django Channels <https://channels.readthedocs.io/en/stable/>`_ to communicate
with the users and utilizes `django-channels-presence <https://django-channels-presence.readthedocs.io/en/latest/>` to
track the participants for a poker session.
