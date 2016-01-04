"""
Establishing referral routes
"""
from opal.utils import camelcase_to_underscore
from opal.core.schemas import serialize_model
from opal.core import app_importer


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
        return app_importer.get_subclass("referrals", klass)

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
