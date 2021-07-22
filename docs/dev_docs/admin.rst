Admin
=====

.. automodule:: planning_poker.admin
   :members:
   :exclude-members: StoryAdmin

.. autoclass:: planning_poker.admin.StoryAdmin
   :members:

   This admin differs from the usual Django admin because it provides the option to add additional admin actions.
   This is used by our Jira extension to allow the user to select stories they want to export the story points for
   and pass them to an action defined in the extension app without tampering with the code defined here.
