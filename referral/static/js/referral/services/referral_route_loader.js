angular.module('opal.referral.services')
    .factory('referralLoader', function($q, $route, $http) {
        return function() {
	    var deferred = $q.defer();
	    $http.get('/api/v0.1/referral/'+$route.current.params.route+'/').then(
                function(resource) {
                    var referral = resource.data;
		    deferred.resolve(referral);
	        }, function() {
		    // handle error better
		    alert('Referral Route data could not be loaded');
	        });
	    return deferred.promise;
        };
    });
