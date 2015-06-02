"""
unittests for referral.routes
"""
from opal.core.test import OpalTestCase

from referral.routes import ReferralRoute

class TestRoute(ReferralRoute):
    name            = 'Test Route'
    description     = 'This is a Route we use for unittests'
    target_teams    = ['test']
    target_category = ['testing']
    success_link    = '/awesome/fun/times/'

class ReferralRouteTestCase(OpalTestCase):

    def test_to_dict(self):
        expected = {
            'name'            : 'Test Route',
            'description'     : 'This is a Route we use for unittests',
            'slug'            : 'test_route',
            'success_link'    : '/awesome/fun/times/',
            'verb'            : 'Refer',
            'past_verb'       : 'Referred',
            'progressive_verb': 'Referring',
        }
        self.assertEqual(expected, TestRoute.to_dict())

