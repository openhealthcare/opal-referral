"""
Plugin definition
"""
from django.conf import settings
from opal.core import plugins

from referral import api
from referral.urls import urlpatterns
from referral.routes import ReferralRoute

DISPLAY_MENU = getattr(settings, 'REFERRAL_MENU_ITEM', True)
if DISPLAY_MENU:
    menuitems = [
        dict(
            href='/referrals/#/', display='Referrals', icon='fa fa-mail-forward',
            activepattern='/referrals', index=2)
    ]
else:
    menuitems = []

class ReferralPortalPlugin(plugins.OpalPlugin):
    """
    Main entrypoint to expose this plugin to the host
    OPAL instance.
    """
    urls = urlpatterns
    javascripts = {
        'opal.referral': [
            'js/referral/app.js',
            'js/referral/services/referral_route_loader.js',
            'js/referral/controllers/list.js',
            'js/referral/controllers/referral.js',
            # 'js/referral/controllers/episode_detail.js',
        ]
    }
    menuitems = menuitems
    apis = api.viewsets()

plugins.register(ReferralPortalPlugin)
