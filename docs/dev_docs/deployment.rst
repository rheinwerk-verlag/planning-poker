Deployment
==========

Since this essentially is a Channels application, you should see
`their docs on deployment <https://channels.readthedocs.io/en/stable/deploying.html>`_ for examples.
But there are a few additional things you should be aware of when you deploy this application.

* .. warning::

     **Do not** use the ``channels.layers.InMemoryChannelLayer`` in your live setup. This should solely be used for a
     test/development setup. See the
     `Channels docs on layers <https://channels.readthedocs.io/en/stable/topics/channel_layers.html>`_ for alternatives.

* Run the worker for the channels you have set up in your ``routing.py``. If you chose to use the same ``routing.py`` as
  specified in the example project, you can run the following command. ::

  $ python manage.py runworker websocket

  See the
  `Channels docs on worker <https://channels.readthedocs.io/en/stable/topics/worker.html#receiving-and-consumers>`_ for
  more information.

* Prune any stale presences periodically. See the :ref:`dev_docs/presence:Presence` section and the
  `django-channels-presence docs <https://django-channels-presence.readthedocs.io/en/latest/usage.html#pruning-stale-connections>`_
  for more information on that.
