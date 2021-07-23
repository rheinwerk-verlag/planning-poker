Presence
========

The :ref:`user_docs/user_interface:Participants List` user interface component uses
`django-channels-presence <https://django-channels-presence.readthedocs.io/en/latest/>`_ for keeping track of all the
currently connected participants of a poker session. Every user sends a ``'heartbeat'`` event every 20 seconds via their
:ref:`dev_docs/consumers:Client-Side` consumer to the server which signals that they're are still participating in the
poker session which then updates a timestamp in the database. Any stale connection, which can occur whenever a client
closes a connection improperly (e.g. by losing connection to the server) have to be regularly pruned in order to
accurately display the list of active participants. See the
`Pruning stale connections <https://django-channels-presence.readthedocs.io/en/latest/usage.html#pruning-stale-connections>`_
section at the ``django-channels-presence`` docs for possible ways to prune stale connections.

Receivers
---------
.. autofunction:: planning_poker.receivers.broadcast_presence
