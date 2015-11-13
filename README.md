Referral Portal plugin for OPAL

This allows users to refer patients to other clinical services.

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

### ReferralRoute.page_title

The title to display in the page banner for your route.

Defaults to 'Referral Portal'

### ReferralRoute.target_teams

The names of the teams to which this route referrs patients.

### ReferralRoute.target_category

The `Episode.category` for our new created episodes. If omitted, this will default to
whatever your `OpalApplication.default_episode_category` is set to.

### ReferralRoute.success_link

Where should users be directed after successfully referring a patient ? 

### ReferralRoute.post_create

A hook function that will be called after your new episode is created.

Use this to manipulate your newly created episode.

For example, one might want to automatically enter stub TODO entries for a particular
referral route.

    class TestRoute(ReferralRoute):
        def post_create(self, episode):
            # Do whatever you like to episode
            return

### ReferralRoute.verb

The verb for the thing this route is doing.

Default = 'Refer'

### ReferralRoute.progressive_verb

The progressive form of the verb this route is doing

Default = 'referring'

### ReferralRoute.past_verb

The past form of the verb this route is doing

Default = 'referred'

## Settings

### REFERRAL_MENU_ITEM

Display a menu Item? 

Defaut = True

## Integrations 

[![Build
Status](https://travis-ci.org/openhealthcare/opal-referral.png?branch=master)](https://travis-ci.org/openhealthcare/opal-referral)

[![Code Health](https://landscape.io/github/openhealthcare/opal-referral/master/landscape.svg?style=flat)](https://landscape.io/github/openhealthcare/opal-referral/master)
