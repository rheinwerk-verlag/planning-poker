Consumers
=========

Communication Between the Consumers
-----------------------------------

There are two consumers for each participant in a poker session in order to communicate between the server and the
client. They talk to each other using messages in JSON format, which always contain the name of the event they want
to trigger at the recipient(s) and any additional data they want to send alongside with the message. The consumers on
both sides provide a method you can use to send an event.

Sample message:

.. code-block:: json

   {
     "type": "send_json",
     "event": "story_changed",
     "data": {
       "id": 2,
       "story_label": "Poker 2: Create Screenshots",
       "description": "<h1>HTML Ipsum</h1>\r\n\r\n<p><strong>Pellentesque habitant morbi</strong>...",
       "votes": {
         "3": [
           {
             "id": 1,
             "name": "JohnDoe"
           }
         ],
         "5": [
           {
             "id": 2,
             "name": "MaxMustermann"
           }
         ]
       }
     }
   }

Both consumers contain an attribute, defining which events will be handled, which can be easily expanded to add
additional features in the future. See the :ref:`dev_docs/consumers:Server-Side` or
:ref:`dev_docs/consumers:Client-Side` consumers for more information on how these attributes are defined.

.. note::

   Consumers in the frontend can only talk to their corresponding consumer on the backend, whereas the consumer on the
   backend can either message all the front end consumers or only send messages to their counterpart.


Server-Side
-----------

.. autoclass:: planning_poker.consumers.PokerConsumer
    :members:
    :show-inheritance:

    Use the provided ``send_event`` method to send events to the client-side consumers. Events are strings signaling a
    specific thing occurred. Any event listeners can then differentiate between different events and perform special
    reactions based on their name.

    These are the events sent by the server by default:

    +------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    | Event Name             | Data                                                                                                                                                                                                                                   |
    |                        +--------------------------------+--------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------+
    |                        | Field Name                     | Example                                                                  | Description                                                                                                                |
    +========================+================================+==========================================================================+============================================================================================================================+
    | story_points_submitted | story_points                   | ``5``                                                                    | The amount of points which should be set                                                                                   |
    +------------------------+--------------------------------+--------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------+
    | story_changed          | id                             | ``1``                                                                    | The id of the story which should be changed to                                                                             |
    |                        +--------------------------------+--------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------+
    |                        | story_label                    | ``"Poker 2: Create Screenshots"``                                        | The label of the story                                                                                                     |
    |                        +--------------------------------+--------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------+
    |                        | description                    | ``"<h1>HTML Ipsum</h1>\r\n\r\n<p><strong>Pellentesque hab..."``          | The description of the story                                                                                               |
    |                        +--------------------------------+--------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------+
    |                        | votes                          | ``{"3": [{"id": 1, "name": "John Doe"}]}``                               | Object where the keys are the story points and their corresponding values are lists of the voters who voted for the option |
    +------------------------+--------------------------------+--------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------+
    | poker_session_ended    | poker_session_end_redirect_url | ``"/poker/"``                                                            | The URL to which the participants of the poker session should be redirected to when the session ends                       |
    +------------------------+--------------------------------+--------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------+
    | participants_changed   | participants                   | ``[{"id": 1, "name": "John Doe"}, {"id": 2, "name": "Max Mustermann"}]`` | An array of user objects with a *unique* id and a username                                                                 |
    +------------------------+--------------------------------+--------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------+

    Expand the ``commands`` dictionary to respond to custom events.


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

.. automodule:: planning_poker.consumers
   :members:
   :exclude-members: PokerConsumer


Client-Side
-----------

.. js:autoclass:: BaseConsumer
   :members:

   The ``BaseConsumer`` and its subclass on the client-side function similarly to the ``PokerConsumer`` on
   the server-side. The same things that were said about the server-side consumer also apply to the client-side
   consumers. Use ``sendEvent`` to send an event to the server and expand ``commands`` to respond to custom events.

   .. attribute:: commands
      :type: Object

      This Object contains the event names as attributes and their corresponding values are the function which should be
      used to handle the data. The data object will be passed as an argument to the handler function.

.. js:autoclass:: PokerConsumer
   :members:

   These are the events sent by the client by default:

   +----------------------+------------------------------------------------------------------------------------------+
   | Event Name           | Data                                                                                     |
   |                      +--------------+---------+-----------------------------------------------------------------+
   |                      | Field Name   | Example | Description                                                     |
   +======================+==============+=========+=================================================================+
   | next_story_requested | story_id     | ``1``   | The id of the story which should be changed to                  |
   +----------------------+--------------+---------+-----------------------------------------------------------------+
   | points_submitted     | story_points | ``"5"`` | The amount of points which should be set                        |
   +----------------------+--------------+---------+-----------------------------------------------------------------+
   | vote_submitted       | choice       | ``"3"`` | The story points the voter voted for                            |
   +----------------------+--------------+---------+-----------------------------------------------------------------+
   | reset_requested      |              |         | No data. Signals the server that the votes should be reset      |
   +----------------------+--------------+---------+-----------------------------------------------------------------+
   | heartbeat            |              |         | No data. Signals the server that the participant still partakes |
   |                      |              |         | in the poker session                                            |
   +----------------------+--------------+---------+-----------------------------------------------------------------+
