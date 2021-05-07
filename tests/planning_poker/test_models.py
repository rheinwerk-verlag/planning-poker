from collections import OrderedDict

import pytest
from django.contrib.auth import get_user_model


@pytest.mark.django_db
class TestStory:
    def test_get_votes_with_voter_information(self, story):
        users = [get_user_model().objects.create(username='user{}'.format(i), password='password') for i in range(1, 4)]
        story.votes.create(user=users[0], choice='2')
        story.votes.create(user=users[1], choice='2')
        story.votes.create(user=users[2], choice='1')

        expected_result = OrderedDict([
            ('2', [{'id': users[0].id, 'name': users[0].username}, {'id': users[1].id, 'name': users[1].username}]),
            ('1', [{'id': users[2].id, 'name': users[2].username}])
        ])

        assert story.get_votes_with_voter_information() == expected_result
