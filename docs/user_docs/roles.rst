.. _roles:

Roles
=====
The participants of a poker session are separated into two groups: `Voter`_ and `Moderator`_. Both these groups perform
different tasks during a poker session and can thus interact with the page differently. A participant can be part of
both groups at the same time and will behave a little bit differently. See `Voter + Moderator`_ for more information.

.. note::
   A user with no assigned role can still spectate a poker session and see the current story and the other participants'
   votes.

Voter
------
The majority of a session's participants are probably Voters. It's their job to discuss and evaluate the scope of story
in order to estimate the amount of points it'll take up during a sprint.

To make an user a voter give them the :code:`Can vote for a story.` permission with the codename :code:`vote`

Moderator
---------
The moderator is responsible for administration the current session. They can skip/choose specific stories to match the
flow of the session, reset the votes if the voters deadlocked themselves in a discussion over a draw, and choose the
final points for a story.

To make an user a moderator give them the :code:`Is able to moderate a planning_poker session.` permission with the
codename :code:`moderate`

Voter + Moderator
-----------------
Sometimes you'll encounter the problem that there is no moderator present and you still want to poker your stories as a
team. In this case someone can take over both roles and simultaneously be a voter and a moderator. They may perform all
actions but some only become available after they have voted.

A user is considered a Voter + Moderator if they have both the permissions of a voter and a moderator.

Permissions
-----------

+------------------+---------+-------------------------+-----------+-------------------------+
|      Action      | No Role |          Voter          | Moderator |    Voter + Moderator    |
+==================+=========+=========================+===========+=========================+
|                                        Stories List                                        |
+------------------+---------+-------------------------+-----------+-------------------------+
|   Choose Story   |    n    |            n            |     y     |            y            |
+------------------+---------+-------------------------+-----------+-------------------------+
|                                        Current Story                                       |
+------------------+---------+-------------------------+-----------+-------------------------+
|  Vote for Points |    n    |            y            |     n     |            y            |
+------------------+---------+-------------------------+-----------+-------------------------+
| Set Story Points |    n    |            n            |     y     |            y            |
|                  |         |                         |           | (after they have voted) |
+------------------+---------+-------------------------+-----------+-------------------------+
|    Reset Votes   |    n    |            n            |     y     |            y            |
+------------------+---------+-------------------------+-----------+-------------------------+
|                                       Votes Overview                                       |
+------------------+---------+-------------------------+-----------+-------------------------+
|     See Votes    |    y    |            y            |     y     |            y            |
|                  |         | (after they have voted) |           | (after they have voted) |
+------------------+---------+-------------------------+-----------+-------------------------+
