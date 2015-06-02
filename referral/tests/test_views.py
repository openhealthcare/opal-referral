"""
Unittests for referral.views
"""
from django.contrib.auth.models import User
from opal.core.test import OpalTestCase

class ReferralIndexTestCase(OpalTestCase):

    def setUp(self):
        self.user2 = User.objects.create_user(username='testuser', password='password')

    def test_index(self):
        self.assertTrue(self.client.login(username='testuser', password='password'))
        self.assertStatusCode('/referrals/', 200)
        
