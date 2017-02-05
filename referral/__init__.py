"""
Package definition
"""
from django.conf import settings
from opal.core import plugins

from referral import api
from referral.urls import urlpatterns
from referral.routes import ReferralRoute
