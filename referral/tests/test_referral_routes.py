"""
unittests for referral.routes
"""
import mock

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

    def test_get(self):
        self.assertEqual(TestRoute, ReferralRoute.get('test_route'))

    @mock.patch.object(Colour, "get_form_url")
    def test_to_dict(self, get_form_url):
        self.maxDiff = None
        get_form_url.return_value = "http://some_url.html"


        expected = {
            'additional_models': [{
                'advanced_searchable': False,
                'angular_service': 'Colour',
                'display_name': 'Colour',
                'fields': [{
                    'model': 'Colour',
                    'default': None,
                    'lookup_list': None,
                    'enum': None,
                    'description': None,
                    'name': 'created',
                    'title': 'Created',
                    'type': 'date_time'},
                           {
                               'model': 'Colour',
                               'default': None,
                               'enum': None,
                               'description': None,
                               'lookup_list': None,
                               'name': 'updated',
                               'title': 'Updated',
                               'type': 'date_time'},
                           {
                               'model': 'Colour',
                               'default': None,
                               'lookup_list': None,
                               'enum': None,
                               'description': None,
                               'name': u'created_by_id',
                               'title': u'Created By',
                               'type': 'forei'},
                           {
                               'model': 'Colour',
                               'lookup_list': None,
                               'enum': None,
                               'description': None,
                               'default': None,
                               'name': u'updated_by_id',
                               'title': u'Updated By',
                               'type': 'forei'},
                           {
                               'model': 'Colour',
                               'lookup_list': None,
                               'enum': None,
                               'description': None,
                               'default': None,
                               'name': 'consistency_token',
                               'title': 'Consistency Token',
                               'type': 'token'},
                           {
                               'model': 'Colour',
                               'lookup_list': None,
                               'enum': None,
                               'description': None,
                               'default': None,
                               'name': 'name',
                               'title': 'Name',
                               'type': 'string'}],
                'name': 'colour',
                'single': False,
                'form_url': "http://some_url.html",
                'icon': 'fa fa-comments'
            }],
            'name': 'Test Route',
            'description': 'This is a Route we use for unittests',
            'slug': 'test_route',
            'verb': 'Refer',
            'past_verb': 'Referred',
            'progressive_verb': 'Referring',
            'page_title': None
        }
        self.assertEqual(expected, TestRoute.to_dict())
