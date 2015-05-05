describe('ReferralCtrl', function (){
    var $controller, $scope, $httpBackend, $rootScope;
    var options, referral_route

    beforeEach(module('opal.referral.controllers'));

    beforeEach(inject(function($injector){
        $rootScope   = $injector.get('$rootScope');
        $scope       = $rootScope.$new();
        $controller  = $injector.get('$controller');
        $httpBackend = $injector.get('$httpBackend');

        referral_route = {
            slug: 'test'
        };
        options = options;

        controller = $controller('ReferralCtrl', {
            $rootScope     : $rootScope,
            options        : options,
            $scope         : $scope,
            referral_route  : referral_route
        });
    }));

    
    describe('new_patient()', function (){
        it('Should set $scope.patient', function () {
            expect($scope.patient).toBe(null);
            $scope.new_patient()
            expect($scope.patient.demographics).toEqual([{}]);
        });
    });
    
    describe('refer()', function (){
        it('Should hit the api', function () {
            $scope.hospital_number = '1234';
            
            $httpBackend.expectPOST('/api/v0.1/referral/test/', {
                hospital_number: '1234',
                demographics   : {}
            }).respond({success: 'YAY'});

            $scope.new_patient();
            $scope.refer();
            $httpBackend.flush();
            
            expect($scope.post_patient_text).toBe(null);
            expect($scope.state).toBe('success');
            
        });
    });
    
});
