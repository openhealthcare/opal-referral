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
