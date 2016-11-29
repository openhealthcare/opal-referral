"""
Unittests for referral.views
"""
from django.contrib.auth.models import User
from mock import patch, MagicMock
from opal.core.test import OpalTestCase

from referral import views

class ReferralIndexTestCase(OpalTestCase):

    def setUp(self):
        self.user2 = User.objects.create_user(username='testuser', password='password')

    # def test_index(self):
    #     self.assertTrue(self.client.login(username='testuser', password='password'))
    #     self.assertStatusCode('/referrals/', 200)


class ReferralTemplateViewTestCase(OpalTestCase):

    def setup_view(self, view):
        v = view()
        r = self.rf.get('hah.html')
        v.request = r
        return v

    def test_dispatch_sets_self_name(self):
        view = self.setup_view(views.ReferralTemplateView)
        view.dispatch(view.request, name='the-name')
        self.assertEqual('the-name', view.name)

    def test_template_names(self):
        view = self.setup_view(views.ReferralTemplateView)
        view.name = 'the_name'
        names = view.get_template_names()
        self.assertEqual(['referral/the_name', 'referral/referral.html'], names)

    @patch('referral.ReferralRoute.list')
    def test_get_context_data_lists_routes(self, mock_list):
        mock_list.return_value = []
        view = self.setup_view(views.ReferralTemplateView)
        ctx = view.get_context_data()
        self.assertEqual([], list(ctx['referral_routes']))
