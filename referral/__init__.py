"""
Plugin definition
"""
from django.conf import settings

from opal.utils import OpalPlugin, stringport

from referral.urls import urlpatterns

# So we only do it once
IMPORTED_FROM_APPS = False

def import_from_apps():
    """
    Iterate through installed apps attempting to import app.wardrounds
    This way we allow our implementation, or plugins, to define their
    own ward rounds. 
    """
    print "Importing from apps"
    for app in settings.INSTALLED_APPS:
        try:
            stringport(app + '.referrals')
        except ImportError:
            pass # not a problem
    global IMPORTED_FROM_APPS
    IMPORTED_FROM_APPS = True
    return

class ReferralPortalPlugin(OpalPlugin):
    """
    Main entrypoint to expose this plugin to the host
    OPAL instance.
    """
    urls = urlpatterns
    javascripts = {
        'opal.referral': [
            'js/referral/app.js',
            # 'js/referral/services/referral_route_loader.js',
            'js/referral/controllers/list.js',
            # 'js/referral/controllers/referral.js',
            # 'js/referral/controllers/episode_detail.js',
        ]
    }
    menuitems = [
        dict(
            href='/referrals/', display='Referrals', icon='fa fa-mail-forward',
            activepattern='/referrals')         
    ]

class ReferralRoute(object):
    """
    Base Referral Route class - individal referral routes should override this.
    """
    name        = 'Please name me Larry!'
    description = 'Please describe me Larry!'

    @classmethod
    def list(klass):
        """
        Return a list of all ward rounds
        """
        if not IMPORTED_FROM_APPS:
            import_from_apps()
        return klass.__subclasses__()
