"""
API for the OPAL referral portal.
"""
from opal.models import Patient
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

class ReferralViewSet(ViewSet):

    def list(self, request):
        return Response(self.referral.to_dict())

    def create(self, request):
        hospital_number = request.data['hospital_number']
        patient, created = Patient.objects.get_or_create(
            demographics__hospital_number=hospital_number
        )
        demographics = patient.demographics_set.get()
        if created:
            demographics.hospital_number = hospital_number
            demographics.save()

        if 'demographics' in request.data:
            demographics.update_from_dict(request.data['demographics'], request.user)

        episode = patient.create_episode()
        if self.referral.target_category:
            episode.category = self.referral.target_category
            episode.save()
        episode.set_tag_names(self.referral.target_teams, request.user)

        self.referral().post_create(episode, request.user)
        return Response({'success': 'YAY'}, status.HTTP_201_CREATED)
    
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
