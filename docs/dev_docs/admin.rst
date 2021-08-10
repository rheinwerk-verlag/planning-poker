Admin
=====

.. autoclass:: planning_poker.admin.StoryAdmin
   :members:

   This admin differs from the usual Django admin because it provides the option to add additional admin actions.
   This can be used by extensions to define custom actions without tampering with the code defined here. Our Jira
   extension utilizes this to allow the user to select stories they want to export the story points for and pass them to
   an action defined in the extension app.

.. automodule:: planning_poker.admin
   :members:
   :exclude-members: StoryAdmin
