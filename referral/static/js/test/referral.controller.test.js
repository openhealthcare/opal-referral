describe('ReferralCtrl', function (){
    var $controller, $scope, $httpBackend, $rootScope;
    var options, referral_route

    beforeEach(module('opal.referral.controllers'));

    beforeEach(inject(function($injector){
        $rootScope   = $injector.get('$rootScope');
        $scope       = $rootScope.$new();
        $controller  = $injector.get('$controller');
        $httpBackend = $injector.get('$httpBackend');

        referral_route = {};
        options = options;

        controller = $controller('ReferralCtrl', {
            $rootScope     : $rootScope,
            options        : options,
            $scope         : $scope,
            referral_route  : referral_route
        });
    }));
    
    
    describe('refer()', function (){
        it('Should hit the api', function () {
            expect(1).toBe(1);
        });
    });
    
});
