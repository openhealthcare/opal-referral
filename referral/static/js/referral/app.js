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

app.run(['$rootScope', 'ngProgressLite', function($rootScope, ngProgressLite) {
    // When route started to change.
    $rootScope.$on('$routeChangeStart', function() {
        ngProgressLite.set(0);
        ngProgressLite.start();
    });

    // When route successfully changed.
    $rootScope.$on('$routeChangeSuccess', function() {
        ngProgressLite.done();
    });

    // When some error occured.
    $rootScope.$on('$routeChangeError', function() {
        ngProgressLite.set(0);
    });
}]);

app.config(function($routeProvider){
    $routeProvider.when('/', {redirectTo: '/list'})
        .when('/list', {
            controller: 'ReferralRouteListCtrl',
            resolve: {},
            templateUrl: '/referral/templates/list.html'
        })
})
