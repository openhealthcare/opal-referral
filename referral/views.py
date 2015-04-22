"""
Views for the OPAL referral portal plugin
"""
from django.views.generic import View, TemplateView

from opal.models import Patient
from opal.core.views import LoginRequiredMixin, _build_json_response, _get_request_data

class ReferralIndexView(LoginRequiredMixin, TemplateView):
    """
    Main entrypoint into the referral portal service. 
    
    Lists our referral routes.
    """
    template_name = 'referral/index.html'


class ReferralView(LoginRequiredMixin, View):
    """
    Return a JSON serialised referral
    """
    def dispatch(self, *args, **kwargs):
        from referral import ReferralRoute
        self.referral = ReferralRoute.get(kwargs['name'])
        if self.referral == None:
            raise ValueError('Invalid referral name larry')
        return super(ReferralView, self).dispatch(*args, **kwargs)
        
    def get(self, *args, **kwargs):
        """
        Return a serialised version of this route's metadata
        """
        serialised = _build_json_response(self.referral.to_dict())
        return serialised

    def post(self, *args, **kwargs):
        """
        Create a new episode for our patient, assign them to the
        target teams.
        """
        data = _get_request_data(self.request)
        hospital_number = data['hospital_number']
        patient, created = Patient.objects.get_or_create(
            demographics__hospital_number=hospital_number
        )
        if created:
            demographics = patient.demographics_set.get()
            demographics.update_from_dict(data['demographics'], self.request.user)

        episode = patient.create_episode()
        if self.referral.target_category:
            episode.category = self.referral.target_category
            episode.save()
        episode.set_tag_names(self.referral.target_teams, self.request.user)
        return _build_json_response({'success': 'Yay'})


class ReferralTemplateView(TemplateView):
    def dispatch(self, *args, **kwargs):
        self.name = kwargs['name']
        return super(ReferralTemplateView, self).dispatch(*args, **kwargs)

    def get_template_names(self, *args, **kwargs):
        return ['referral/'+self.name]

    def get_context_data(self, *args, **kwargs):
        context = super(ReferralTemplateView, self).get_context_data(**kwargs)
        from referral import ReferralRoute
        context['referral_routes'] = ReferralRoute.list()
        return context
