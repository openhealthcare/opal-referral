Referral Portal plugin for OPAL

This allows users to refer patients to other clinical services.

[![Build
Status](https://travis-ci.org/openhealthcare/opal-referral.png?branch=v0.3.0)](https://travis-ci.org/openhealthcare/opal-referral)

[![Coverage Status](https://coveralls.io/repos/github/openhealthcare/opal-referral/badge.svg?branch=v0.3.0)](https://coveralls.io/github/openhealthcare/opal-referral?branch=v0.3.0)

## Defining a referral Route.

We expect referral routes to be located in `yourapp.referrals`.

In order to define a referral route, we subclass `referral.routes.ReferralRoute`.

```python
class TestRoute(ReferralRoute):
    name            = 'Test Route'
    description     = 'This is a Route we use for unittests'
    target_teams    = ['test']
    target_category = ['testing']
    success_link    = '/awesome/fun/times/'

        def post_create(self, episode): pass
```

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

```python
class TestRoute(ReferralRoute):
    def post_create(self, episode):
        # Do whatever you like to episode
        return
```

### ReferralRoute.verb

The verb for the thing this route is doing.

Default = 'Refer'

### ReferralRoute.progressive_verb

The progressive form of the verb this route is doing

Default = 'referring'

### ReferralRoute.past_verb

The past form of the verb this route is doing

Default = 'referred'

## Adding additional models

Additional models can also be added to the referral app for creation upon referral.
By default we only add a patient, if you'd like to add additional models add them
as part of additional_models. Then add template that in {{ app }}/referral/{{ route.name }}
this template should extend referral/referral.html.

```python
class TestRoute(ReferralRoute):
    name            = 'Test Route'
    additional_models = [
        models.Diagnosis,
        models.Treatments
    ]
```

The additional models will be displayed after patient details, in the order they
appear in routes. The template should show titles/forms when scope.state is pointing
to the name of the label.

```html
    {% block additional_models %}
    <div ng-show="state=='diagnosis'">
        <form class="form-horizontal">
            {% input label="Condition" model="additionalModelsData.diagnosis.condition" lookuplist="condition_list" %}
        </form>

        <button class="btn btn-lg btn-primary pull-right" ng-click="nextStep()">
            <i class="fa fa-arrow-right"></i>
            <span ng-show="!getNextStep()">[[ route.verb ]] to [[ route.name ]]</span>
            <span ng-show="getNextStep()">[[ getNextStep().display_name ]]</span>
        </button>
    </div>
    ...
    {% endblock %}
```

## Customising the template for your referral route

By default we look for a custom template named `'referral/{0}.html'.format(ReferralRoute.name)` to render the detail
of the route. Extending 'referral/referral.html' should be straightforward and allow you to customise specific
blocks.

## Settings

### REFERRAL_MENU_ITEM

Display a menu Item?

Defaut = True
