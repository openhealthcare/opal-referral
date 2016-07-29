"""
API for the OPAL referral portal.
"""
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from opal.models import Patient

class ReferralViewSet(ViewSet):

    def list(self, request):
        return Response(self.referral.to_dict())

    def create(self, request):
        hospital_number = request.data['hospital_number']
        patient, created = Patient.objects.get_or_create(
            demographics__hospital_number=hospital_number
        )
        demographics = patient.demographics_set.get()
        target_teams = set(self.referral.target_teams)
        if created:
            demographics.hospital_number = hospital_number
            demographics.save()

        if 'demographics' in request.data:
            demographics.update_from_dict(
                request.data['demographics'], request.user
            )

        # we should never, even accidentally have a patient without an episode
        if self.referral.create_new_episode or not patient.episode_set.count():
            episode = patient.create_episode()
        else:
            episode = patient.episode_set.order_by("-created").first()
            target_teams = target_teams.union(episode.get_tag_names(request.user))

        for additional_model in self.referral.additional_models:
            model_name = additional_model.__name__.lower()

            if model_name in request.data:
                new_model = additional_model()
                data_dict = request.data[model_name]
                data_dict["episode_id"] = episode.id
                new_model.update_from_dict(data_dict, request.user)

        if self.referral.target_category:
            episode.category_name = self.referral.target_category
            episode.save()
        episode.set_tag_names(list(target_teams), request.user)
        referral = self.referral()
        referral.post_create(episode, request.user)
        success_link = referral.get_success_link(episode)
        self.referral().post_create(episode, request.user)
        return Response({'success_link': success_link}, status.HTTP_201_CREATED)


def viewsets():
    """
    Return our api viewsets
    """
    from referral import ReferralRoute

    apis = []
    for route in ReferralRoute.list():
        class RouteAPI(ReferralViewSet):
            referral = route
            base_name = 'referral/'+route.slug()

        apis.append(('referral/'+route.slug(), RouteAPI))
    return apis
