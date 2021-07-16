Consumers
=========

Server-Side
-----------

.. autoclass:: planning_poker.consumers.PokerConsumer
    :members:
    :show-inheritance:

    Use the provided ``send_event`` method to send events to the client-side consumers. ``Events`` are strings used to
    determine how the included data should be handled. Expand the ``self.commands`` dictionary to respond to custom
    events.

    .. attribute:: commands
       :type: Dict[str, Dict[str, Any]]

       This dictionary maps the events to another dictionary which has exactly two keys.

       - ``'method'`` determines which method should be called to handle the data (e.g. ``self.reset_requested``). Its
         value can be any callable. Any data passed along with the event will be passed into the callable as keyword
         arguments.

       - ``'required_permission'`` restricts which users can respond to this event. Its value is either a Django
         permission string (e.g. ``MODERATE_PERMISSION``) which will be used to evaluate the user's permission via
         ``user.has_perm(required_permission)`` to see whether they are allowed to respond to the event or ``None`` if
         no permission is required.


Client-Side
-----------

The PokerConsumer on the client-side functions similarly to the consumer on the server-side. The same things that were
said about the server-side consumer also apply to the client-side consumer. Use ``sendEvent`` to send an event to the
server and expand ``this.commands`` to respond to custom events.

.. js:autoclass:: PokerConsumer
   :members:
