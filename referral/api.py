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

