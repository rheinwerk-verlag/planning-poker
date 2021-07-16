Models
======

.. autoclass:: planning_poker.models.Story
   :members:
   :exclude-members: DoesNotExist, MultipleObjectsReturned

   .. attribute:: ticket_number
      :type: django.db.models.CharField

      The ticket number. Used for displaying the story to the user.

   .. attribute:: title
      :type: django.db.models.CharField

      The title. Used for displaying the story to the user.

   .. attribute:: description
      :type: django.db.models.TextField

      The description. Main source of information about the story for the user.

   .. attribute:: story_points
      :type: django.db.models.PositiveSmallIntegerField

      The estimated story points. The possible values are :ref:`dev_docs/constants:Fibonacci Choices` and ``None``.

   .. attribute:: poker_session
      :type: django.db.models.ForeignKey

      The poker session to which the story belongs to.

.. autoclass:: planning_poker.models.PokerSession
   :members:
   :exclude-members: DoesNotExist, MultipleObjectsReturned

   .. attribute:: poker_date
      :type: django.db.models.DateField

      The date on which the poker session takes place.

   .. attribute:: name
      :type: django.db.models.CharField

      The name. Used solely for displaying the poker session to the user.

   .. attribute:: active_story
      :type: django.db.models.OneToOneField

      The story which is currently active in this poker session. This is used to determine which story should currently
      be displayed in the user interface.

.. autoclass:: planning_poker.models.Vote
   :members:
   :exclude-members: DoesNotExist, MultipleObjectsReturned

   .. attribute:: story
      :type: django.db.models.ForeignKey

      The story to which this vote belongs to.

   .. attribute:: user
      :type: django.db.models.ForeignKey

      The user who casted this vote.

   .. attribute:: choice
      :type: django.db.models.CharField

      The option which was voted for. See :ref:`dev_docs/constants:All Voting Options` for all possible values.
