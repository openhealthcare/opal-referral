"""
Urls for the OPAL referrals plugin
"""
from django.conf.urls import patterns, url

from referral import views

urlpatterns = patterns(
    '',
    url('^referrals/$', views.ReferralIndexView.as_view()),
    # url('^referral/(?P<name>[a-z_]+)$', views.ReferralView.as_view()),
    # url(r'^referral/templates/episode_detail.html$',
    #     views.ReferralEpisodeDetailTemplateView.as_view()),
    # url(r'^referral/templates/(?P<referral_name>[a-z_]+)/episode_detail.html$',
    #     views.ReferralEpisodeDetailTemplateView.as_view()),
    url(r'^referral/templates/(?P<name>[a-z_]+.html)$',
        views.ReferralTemplateView.as_view()),
    # url(r'^referral/templates/(?P<referral_name>[a-z_]+)/(?P<name>[a-z_]+.html)$',
    #     views.ReferralTemplateView.as_view()),
)
