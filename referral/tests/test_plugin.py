"""
Unittest for plugin
"""
from opal.core.test import OpalTestCase

from referral import plugin

class PluginTestCase(OpalTestCase):
    def test_javascripts(self):
        j = plugin.ReferralPortalPlugin.javascripts
        self.assertIn('js/referral/app.js', j['opal.referral'])
