Referral Portal plugin for OPAL

## Defining a referral Route.

We expect referral routes to be located in `yourapp.referrals`.

In order to define a referral route, we subclass `referral.routes.ReferralRoute`.

    class TestRoute(ReferralRoute):
        name            = 'Test Route'
        description     = 'This is a Route we use for unittests'
        target_teams    = ['test']
        target_category = ['testing']
        success_link    = '/awesome/fun/times/'

        def post_create(self, episode): pass

### ReferralRoute.name

The name of your referral route.

### ReferralRoute.description

The description of your referral route

### ReferralRoute.target_teams

The names of the teams to which this route referrs patients.

### ReferralRoute.target_category

The `Episode.category` for our new created episodes. If omitted, this will default to
whatever your `OpalApplication.default_episode_category` is set to.

### ReferralRoute.success_link

Where should users be directed after successfully referring a patient ? 

### ReferralRoute.post_create 

A hook function that will be called after your new episode is created.

Use this to manipulate your newly created episode before it is serialised and returned to the
referring user.

## Integrations 

[![Build
Status](https://travis-ci.org/openhealthcare/opal-referral.png?branch=master)](https://travis-ci.org/openhealthcare/elcid)
