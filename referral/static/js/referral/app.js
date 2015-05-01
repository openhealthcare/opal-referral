//
// Main OPAL Referrals plugin application!
//
var opalshim = OPAL.module('opal', [])
var services = OPAL.module('opal.referral.services', []);

var controllers = OPAL.module('opal.referral.controllers', [
    'opal.services',
    'opal.referral.services'
]);

var app = OPAL.module('opal.referral', [
    'ngRoute',
    'ngProgressLite',
    'ngCookies',
    'opal.filters',
    'opal.services',
    'opal.directives',
    'opal.controllers',
    'opal.referral.controllers'
]);

OPAL.run(app);

app.config(function($routeProvider){
    $routeProvider.when('/', {redirectTo: '/list'})
        .when('/list', {
            controller: 'ReferralRouteListCtrl',
            resolve: {},
            templateUrl: '/referral/templates/list.html'
        })
        .when('/:route', {
            controller: 'ReferralCtrl',
            resolve: {
                referral_route: function(referralLoader){ return referralLoader() },
		options: function(Options) { return Options; },
                
            },
            templateUrl: function(params){
                return '/referral/templates/referral.html'
            }
        })
})
