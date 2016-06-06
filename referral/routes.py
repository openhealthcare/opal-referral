"""
Establishing referral routes
"""
from django.conf import settings

from opal.utils import stringport, camelcase_to_underscore, _itersubclasses
from opal.core.schemas import serialize_model

# So we only do it once
IMPORTED_FROM_APPS = False


def import_from_apps():
    """
    Iterate through installed apps attempting to import app.wardrounds
    This way we allow our implementation, or plugins, to define their
    own ward rounds.
    """
    for app in settings.INSTALLED_APPS:
        try:
            stringport(app + '.referrals')
        except ImportError:
            pass # not a problem
    global IMPORTED_FROM_APPS
    IMPORTED_FROM_APPS = True
    return


class ReferralRoute(object):
    """
    Base Referral Route class - individal referral routes should override this.
    """
    name         = 'Please name me Larry!'
    description  = 'Please describe me Larry!'
    target_teams = []
    target_category = None
    success_link = None
    page_title = None
    verb = 'Refer'
    progressive_verb = 'Referring'
    past_verb = 'Referred'
    create_new_episode = True
    additional_models = []

    @classmethod
    def get(klass, name):
        """
        Return a specific referral route by slug
        """
        for sub in klass.list():
            if sub.slug() == name:
                return sub

    @classmethod
    def list(klass):
        """
        Return a list of all ward rounds
        """

        if not IMPORTED_FROM_APPS:
            import_from_apps()
        return _itersubclasses(klass)

    @classmethod
    def slug(klass):
        return camelcase_to_underscore(klass.name).replace(' ', '')

    @classmethod
    def to_dict(klass):
        """
        Serialise referral routes for the client
        """
        return dict(
            name=klass.name,
            description=klass.description,
            slug=klass.slug(),
            verb=klass.verb,
            progressive_verb=klass.progressive_verb,
            past_verb=klass.past_verb,
            page_title=klass.page_title,
            additional_models=[
                serialize_model(m) for m in klass.additional_models
            ]
        )

    def post_create(self, episode, user):
        """
        Subclasses should override this method to manipulate an episode
        immediately after it has been created.
        """
        return

    def get_success_link(self, episode):
        return self.success_link
