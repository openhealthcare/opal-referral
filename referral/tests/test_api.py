"""
Unittests for referral.views
"""
import json
import time

from django.test import RequestFactory
from opal.core.test import OpalTestCase
from opal.models import Patient, Episode
from mock import MagicMock

from referral import api
from referral.routes import ReferralRoute

class TestRoute(ReferralRoute):
    name            = 'View Test Route'
    description     = 'This is a Route we use for unittests'
    target_teams    = ['test']
    target_category = ['testing']
    success_link    = '/awesome/fun/times/'


class ReferralViewTestCase(OpalTestCase):
    def setUp(self):
        for name, viewset in api.viewsets():
            if viewset.referral == TestRoute:
                self.viewset = viewset
                break
        self.request = RequestFactory().post('/referral/refer')
        self.patient = Patient.objects.create()
        self.episode = Episode.objects.create(patient=self.patient)
        self.demographics = self.patient.demographics_set.get()
        self.demographics.hospital_number = str(time.time())
        self.demographics.save()
        
    def test_retrieve_gets_route(self):
        route = self.viewset().list(None)
        expected = {
            'name'        : 'View Test Route',
            'description' : 'This is a Route we use for unittests',
            'slug'        : 'view_test_route',
            'success_link': '/awesome/fun/times/'
        }
        self.assertEqual(expected, route.data)

    def test_refer_creates_new_episode(self):
        mock_request = MagicMock(name='Mock request')
        mock_request.data = {
            'hospital_number': self.demographics.hospital_number
            }
        self.assertEqual(1, self.patient.episode_set.count())
        response = self.viewset().create(mock_request)
        self.assertEqual(201, response.status_code)
        self.assertEqual(2, self.patient.episode_set.count())

    def test_refer_creates_new_patient(self):
        pass

    def test_refer_updates_demographics(self):
        pass

    def test_refer_creates_correct_episode_category(self):
        pass

    def test_refer_sets_tag_names(self):
        pass
        
    def test_refer_calls_post_create(self):
        pass
