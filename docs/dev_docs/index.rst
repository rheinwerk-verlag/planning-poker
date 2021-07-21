Developer Documentation
=======================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   admin
   consumers
   models
   views
   presence
   constants
   setup

Development
-----------

The Planning Poker app can be used and expanded like any other Django app. If you want to extend this app's
functionality, you should consider writing an extension app. Feel free and see the
`Jira extension <https://github.com/rheinwerk-verlag/planning-poker-jira>`_ for inspiration on how to design your
extension.

One thing that might be special in this project is that the Django backend can communicate with the users' clients via
websockets provided by `Django Channels <https://channels.readthedocs.io/en/stable/>`_.
