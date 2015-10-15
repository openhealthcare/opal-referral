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
            'additional_models': [{
                'advanced_searchable': False,
                'display_name': 'Colour',
                'fields': [{'lookup_list': None,
                            'name': 'created',
                            'title': 'Created',
                            'type': 'date_time'},
                           {'lookup_list': None,
                            'name': 'updated',
                            'title': 'Updated',
                            'type': 'date_time'},
                           {'lookup_list': None,
                            'name': u'created_by_id',
                            'title': u'Created By Id',
                            'type': 'forei'},
                           {'lookup_list': None,
                            'name': u'updated_by_id',
                            'title': u'Updated By Id',
                            'type': 'forei'},
                           {'lookup_list': None,
                            'name': 'consistency_token',
                            'title': 'Consistency Token',
                            'type': 'token'},
                           {'lookup_list': None,
                            'name': 'name',
                            'title': 'Name',
                            'type': 'string'}],
                'name': 'colour',
                'single': False
            }],
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
