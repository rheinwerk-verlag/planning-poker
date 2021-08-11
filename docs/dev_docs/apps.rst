Apps
====

.. autoclass:: planning_poker.apps.ChannelsPresenceConfig
   :members:
   :undoc-members:

   This has to be currently overridden because
   `django-channels-presence <https://github.com/mitmedialab/django-channels-presence>`_'s app config's
   `name <https://github.com/mitmedialab/django-channels-presence/blob/bcc9f71ca2162d8d8539466ad9787715d43c0faf/channels_presence/apps.py#L5>`_
   is different from the name of the python package, which leads to an ``ImportError`` when Django tries to populate
   the installed apps. This config can be removed once it is fixed upstream.


.. automodule:: planning_poker.apps
   :members:
   :undoc-members:
   :exclude-members: ChannelsPresenceConfig

