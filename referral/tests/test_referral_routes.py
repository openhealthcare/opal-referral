"""
unittests for referral.routes
"""
from opal.core.test import OpalTestCase

from referral.routes import ReferralRoute
from opal.tests.models import Colour


class TestRoute(ReferralRoute):
    name = 'Test Route'
    description = 'This is a Route we use for unittests'
    target_teams = ['test']
    target_category = ['testing']
    success_link = '/awesome/fun/times/'
    additional_models = [Colour]


class ReferralRouteTestCase(OpalTestCase):

    def test_to_dict(self):
        expected = {
            'additional_models': [("Colour", [
                {'lookup_list': None, 'type': 'date_time', 'name': 'created', 'title': 'Created'},
                {'lookup_list': None, 'type': 'date_time', 'name': 'updated', 'title': 'Updated'},
                {'lookup_list': None, 'type': 'forei', 'name': u'created_by_id', 'title': u'Created By Id'},
                {'lookup_list': None, 'type': 'forei', 'name': u'updated_by_id', 'title': u'Updated By Id'},
                {'lookup_list': None, 'type': 'token', 'name': 'consistency_token', 'title': 'Consistency Token'},
                {'lookup_list': None, 'type': 'string', 'name': 'name', 'title': 'Name'}
            ])],
            'name': 'Test Route',
            'description': 'This is a Route we use for unittests',
            'slug': 'test_route',
            'success_link': '/awesome/fun/times/',
            'verb': 'Refer',
            'past_verb': 'Referred',
            'progressive_verb': 'Referring',
            'page_title': None
        }

        self.assertEqual(expected, TestRoute.to_dict())
