Roles
=====
The participants of a poker session are separated into two groups: `Voter`_ and `Moderator`_. Both these groups perform
different tasks during a poker session and can thus interact with the page differently. A participant can be part of
both groups at the same time and will behave a little bit differently. See `Voter + Moderator`_ for more information.

To make a user part of a group give them the corresponding permission in the Django admin. Which permission is required
for a specific group is explained in the following two sections.

.. note::
   A user with no assigned role can still spectate a poker session and see the current story and the other participants'
   votes.

Voter
-----
The majority of a session's participants are probably voters. It's their job to discuss and evaluate the scope of a
story in order to estimate the amount of points it'll take up during a sprint.

To make a user a voter, give them the ``Can vote for a story.`` permission with the codename ``vote``.

Moderator
---------
The moderator is responsible for administrating the current session. They can skip/choose specific stories to match the
flow of the session, reset the votes if the voters deadlocked themselves in a discussion over a draw, and choose the
final points for a story.

To make a user a moderator, give them the ``Is able to moderate a planning_poker session.`` permission with the codename
``moderate``.

Voter + Moderator
-----------------
It is not necessary for you to have a dedicated moderator. Someone can take over both roles and simultaneously be a
voter and a moderator. They may perform all actions but some only become available after they have voted.

A user is considered a Voter + Moderator if they have both the permissions of a voter and a moderator.

Permissions
-----------

+------------------------+---------+---------------------------+-----------+---------------------------+
|      Action            | No Role |          Voter            | Moderator |    Voter + Moderator      |
+========================+=========+===========================+===========+===========================+
|                                        Stories List                                                  |
+------------------------+---------+---------------------------+-----------+---------------------------+
|   Choose Story         | 🚫      | 🚫                        | ✅        | ✅                        |
+------------------------+---------+---------------------------+-----------+---------------------------+
|                                        Current Story                                                 |
+------------------------+---------+---------------------------+-----------+---------------------------+
|  Vote for Points       | 🚫      | ✅                        | 🚫        | ✅                        |
+------------------------+---------+---------------------------+-----------+---------------------------+
| Set Final Story Points | 🚫      | 🚫                        | ✅        | ✅ (after they have voted)|
+------------------------+---------+---------------------------+-----------+---------------------------+
|    Reset Votes         | 🚫      | 🚫                        | ✅        | ✅                        |
+------------------------+---------+---------------------------+-----------+---------------------------+
|                                       Votes Overview                                                 |
+------------------------+---------+---------------------------+-----------+---------------------------+
|     See Votes          | ✅      | ✅ (after they have voted)| ✅        | ✅ (after they have voted)|
+------------------------+---------+---------------------------+-----------+---------------------------+
