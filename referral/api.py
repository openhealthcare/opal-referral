"""
API for the OPAL referral portal.
"""
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

class ReferralViewSet(ViewSet):

    def list(self, request):
        return Response(self.referral.to_dict())

def viewsets():
    """
    Return our api viewsets
    """
    from referral import ReferralRoute
    
    apis = []
    for route in ReferralRoute.list():
        class RouteAPI(ReferralViewSet):
            referral  = route
            base_name = 'referral/'+route.slug()

        apis.append(('referral/'+route.slug(), RouteAPI))
    return apis



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
"""
