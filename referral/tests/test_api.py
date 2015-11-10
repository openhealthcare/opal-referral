"""
Unittests for referral.views
"""
import json
import time

from django.test import RequestFactory
from opal.core.test import OpalTestCase
from opal.models import Patient, Episode, Team
from mock import MagicMock, patch

from referral import api
from referral.routes import ReferralRoute

class TestRoute(ReferralRoute):
    name            = 'View Test Route'
    description     = 'This is a Route we use for unittests'
    target_teams    = ['test']
    target_category = 'testing'
    success_link    = '/awesome/fun/times/'

    def post_create(self, episode, user):
        return


class TestDontCreate(TestRoute):
    name            = "View Don't create Test Route"
    create_new_episode = False


class ReferralViewTestCase(OpalTestCase):
    def setUp(self):
        self.test_team = Team.objects.get_or_create(name='test')
        for name, viewset in api.viewsets():
            if viewset.referral == TestRoute:
                self.viewset = viewset
            if viewset.referral == TestDontCreate:
                self.dont_create_viewset = viewset

        self.request = RequestFactory().post('/referral/refer')
        self.patient = Patient.objects.create()
        self.episode = Episode.objects.create(patient=self.patient)
        self.demographics = self.patient.demographics_set.get()
        self.demographics.hospital_number = str(time.time())
        self.demographics.save()

    def test_retrieve_gets_route(self):
        route = self.viewset().list(None)
        expected = {
            'additional_models': [],
            'name': 'View Test Route',
            'description': 'This is a Route we use for unittests',
            'slug': 'view_test_route',
            'success_link': '/awesome/fun/times/',
            'verb': 'Refer',
            'past_verb': 'Referred',
            'progressive_verb': 'Referring',
            'page_title': None

        }
        self.assertEqual(expected, route.data)

    def test_refer_creates_new_episode(self):
        mock_request = MagicMock(name='Mock request')
        mock_request.data = {
            'hospital_number': self.demographics.hospital_number
        }
        mock_request.user = self.user
        self.assertEqual(1, self.patient.episode_set.count())
        response = self.viewset().create(mock_request)
        self.assertEqual(201, response.status_code)
        self.assertEqual(2, self.patient.episode_set.count())

    def test_refer_creates_new_patient(self):
        mock_request = MagicMock(name='Mock request')
        new_number = 'n' + str(time.time())
        mock_request.data = {
            'hospital_number': new_number,
            }
        mock_request.user = self.user
        self.assertEqual(0, Patient.objects.filter(demographics__hospital_number=new_number).count())
        response = self.viewset().create(mock_request)
        self.assertEqual(201, response.status_code)
        self.assertEqual(1, Patient.objects.filter(demographics__hospital_number=new_number).count())

    def test_refer_updates_demographics(self):
        mock_request = MagicMock(name='Mock request')
        mock_request.data = {
            'hospital_number': self.demographics.hospital_number,
            'demographics'   : {
                'name': 'Test Patient'
            }
        }
        mock_request.user = self.user
        self.assertEqual('', self.patient.demographics_set.get().name)
        response = self.viewset().create(mock_request)
        self.assertEqual('Test Patient', self.patient.demographics_set.get().name)

    def test_refer_creates_correct_episode_category(self):
        mock_request = MagicMock(name='Mock request')
        mock_request.data = {
            'hospital_number': self.demographics.hospital_number
        }
        mock_request.user = self.user
        self.assertEqual(0, self.patient.episode_set.filter(category='testing').count())
        response = self.viewset().create(mock_request)
        self.assertEqual(1, self.patient.episode_set.filter(category='testing').count())

    def test_refer_sets_tag_names(self):
        mock_request = MagicMock(name='Mock request')
        mock_request.data = {
            'hospital_number': self.demographics.hospital_number
        }
        mock_request.user = self.user
        response = self.viewset().create(mock_request)
        episode = self.patient.episode_set.get(category='testing')
        self.assertEqual(['test'], episode.get_tag_names(None))

    def test_refer_calls_post_create(self):
        mock_request = MagicMock(name='Mock request')
        mock_request.data = {
            'hospital_number': self.demographics.hospital_number
        }
        mock_request.user = self.user
        with patch.object(TestRoute, 'post_create') as mock_create:
            response = self.viewset().create(mock_request)
            episode = self.patient.episode_set.get(category='testing')
            mock_create.assert_called_with(episode, mock_request.user)

    def test_dont_create(self):
        old_team = Team.objects.get_or_create(name='old_team')
        self.episode.tagging_set.create(team=old_team)
        mock_request = MagicMock(name='Mock request')
        mock_request.data = {
            'hospital_number': self.demographics.hospital_number
        }
        mock_request.user = self.user
        self.assertEqual(1, self.patient.episode_set.count())
        response = self.viewset().create(mock_request)
        self.assertEqual(201, response.status_code)
        self.assertEqual(1, self.patient.episode_set.count())
        new_team_names = set(self.episode.get_tag_names(self.user))
        self.assertEqual(new_team_names, {'old_team', 'test'})
