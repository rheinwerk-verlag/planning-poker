Constants
=========

The Planning Poker app uses these constants for the choices defined in the :ref:`dev_docs/models:Models` fields.

Fibonacci Choices
-----------------

.. code-block:: python

   FIBONACCI_CHOICES = [
       ('1', '1'),
       ('2', '2'),
       ('3', '3'),
       ('5', '5'),
       ('8', '8'),
       ('13', '13'),
       ('21', '21'),
       ('34', '34'),
   ]

Non Point Options
-----------------

.. code-block:: python

   TOO_LARGE = 'Too large'
   NO_IDEA = 'No idea'

   NON_POINT_OPTIONS = [
       (TOO_LARGE, _('Too large')),
       (NO_IDEA, _('No idea'))
   ]

All Voting Options
------------------

.. code-block:: python

   ALL_VOTING_OPTIONS = FIBONACCI_CHOICES + NON_POINT_OPTIONS
