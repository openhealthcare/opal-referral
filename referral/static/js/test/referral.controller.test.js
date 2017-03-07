describe('ReferralCtrl', function (){
    "use strict";

    var $controller, $scope, $httpBackend, $rootScope;
    var referral_route, controller, Item;

    var referencedata = {
        toLookuplists: function(){return {};}
    };

    var columnSchema = {
      fields: [{
        name: 'name',
        type: "string"
      }]
    };


    beforeEach(module('opal.services'));
    beforeEach(module('opal.referral.controllers'));

    beforeEach(inject(function($injector){
        $rootScope   = $injector.get('$rootScope');
        $rootScope.fields = {name: 'Hat', fields: columnSchema};
        $scope       = $rootScope.$new();
        $controller  = $injector.get('$controller');
        $httpBackend = $injector.get('$httpBackend');
        Item = $injector.get('Item');

        referral_route = {
            slug: 'test'
        };
        referencedata = referencedata;


        controller = $controller('ReferralCtrl', {
            $rootScope     : $rootScope,
            referencedata  : referencedata,
            $scope         : $scope,
            referral_route  : referral_route,
            recordFields: {then: function(){}}
        });
    }));

    describe('newPatient()', function (){
        it('Should set $scope.patient', function () {
            expect($scope.patient).toBe(null);
            $scope.newPatient();
            expect($scope.patient.demographics).toEqual([{}]);
            expect($scope.state).toEqual("editing_demographics");
        });
    });

    describe('newForPatient()', function (){
        it('Should set $scope.patient', function () {
            expect($scope.patient).toBe(null);
            var patient = {demographics: [{first_name: "Sue"}]}
            $scope.newForPatient(patient);
            expect($scope.patient.demographics).toEqual([{first_name: "Sue"}]);
            expect($scope.state).toEqual("has_demographics");
        });
    });

    describe('mergePatient()', function (){
        it('Should set $scope.patient', function () {
            expect($scope.patient).toBe(null);
            var patient = {
                demographics: [{first_name: "Sue", hospital_number: "10"}],
                merged: [{demographics: [{first_name: "Sue"}] } ]
            };
            $scope.mergePatient(patient);
            expect($scope.patient.demographics).toEqual([{first_name: "Sue"}] );
            expect($scope.patient.old_hospital_number).toEqual("10");
        });
    });

    describe('refer()', function (){
        it('Should hit the api', function () {
            $scope.hospital_number = '1234';
            $httpBackend.expectGET('/api/v0.1/userprofile/').respond({});
            $httpBackend.expectPOST('/api/v0.1/referral/test/', {
                hospital_number: '1234',
                demographics   : {},
                Hat: {name: "bowler"}
            }).respond({success_link: '/#/something'});

            $scope.newPatient();
            $scope.additionalModelsData = {Hat: new Item({name: "bowler"}, null, columnSchema)};
            // spyOn($scope.additionalModelsData.Hat, "makeCopy").and.returnValue({
            //   "name": "bowler"
            // });
            $scope.refer();
            $httpBackend.flush();

            expect($scope.post_patient_text).toBe(null);
            expect($scope.state).toBe('success');
            expect($scope.success_link).toBe('/#/something');

        });
    });

});
