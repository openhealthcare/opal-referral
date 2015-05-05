"""
Urls for the OPAL referrals plugin
"""
from django.conf.urls import patterns, url

from referral import views

urlpatterns = patterns(
    '',
    url('^referrals/$', views.ReferralIndexView.as_view()),
    url(r'^referral/templates/(?P<name>[a-z_]+.html)$',
        views.ReferralTemplateView.as_view()),
)
