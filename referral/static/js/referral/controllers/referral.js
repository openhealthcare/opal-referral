//
// Referr a patient
//
angular.module('opal.referral.controllers').controller(
    'ReferralCtrl', function($rootScope, $scope, $http, FieldTranslater,
                             Episode, options, recordFields,
                             referral_route, Item){

        "use strict";
        $scope.route = referral_route;

        // Known states are:
        // Initial -> editing_demographics -> has_demographics -> success
        $scope.state = 'initial';
        $scope.hospital_number = null;
        $scope.patient = null;
        $scope.additionalModelsData = {};

        var cleanAdditionalModelData = function(){
            _.each(referral_route.additional_models, function(am){
                $scope.additionalModelsData[am.name] = new Item({}, undefined, {fields: am.fields});
            });
        };

        cleanAdditionalModelData();

        $scope.additionalModels = referral_route.additional_models;

        //
        // Make our lookuplists available
        //
      	for (var name in options) {
      	    $scope[name + '_list'] = options[name];
      	}

        $scope.lookup_hospital_number = function() {
            var patientFound = function(result){
              if(result.merged && result.merged.length){
                $scope.mergePatient(result);
              }
              else{
                $scope.newForPatient(result);
              }
            };

            Episode.findByHospitalNumber(
                $scope.hospital_number,
                {
                    newPatient:    $scope.newPatient,
                    newForPatient: patientFound,
                    error        : function(){
                        // This shouldn't happen, but we should probably handle it better
                        alert('ERROR: More than one patient found with hospital number');
                    }
                });
        };

        $scope.newPatient = function(result){
            $scope.patient = {
                demographics: [{}]
            };
            $scope.state = 'editing_demographics';
        };

        $scope.newForPatient = function(patient){
            $scope.patient = patient;
            $scope.state   = 'has_demographics';
        };

        $scope.mergePatient = function(patient){
            $scope.patient = patient.merged[0];
            $scope.patient.old_hospital_number = patient.demographics[0].hospital_number;
            $scope.state   = 'merge_demographics';
        };

        // we allow the inclusion of additional steps, if additional steps don't exist
        // we can just go ahead and refer
        $scope.getNextStep = function(){
            var currentIndex;

            if(!$scope.additionalModels.length){
                return null;
            }

            if($scope.state == _.last($scope.additionalModels).name){
                return null;
            }

            currentIndex = _.findIndex($scope.additionalModels, function(am){
                return am.name == $scope.state;
            });

            if(currentIndex === -1){
                return $scope.additionalModels[0];
            }
            else{
                return $scope.additionalModels[currentIndex + 1];
            }
        };

        $scope.nextStep = function(){
            var nextStep = $scope.getNextStep();
            if(!nextStep){
                $scope.refer();
            }
            else{
                $scope.state = nextStep.name;
            }
        };

        $scope.currentAdditionalData = function(){
            return _.find($scope.additionalModels, function(am){
                return am.name === $scope.state ;
            });
        };

        $scope.refer = function(){

            // copy demographics to the toSave object
            var toSave = {
              hospital_number: $scope.hospital_number,
              demographics: FieldTranslater.jsToSubrecord($scope.patient.demographics[0], "demographics")
            }

            // copy additional models to the toSave object
            if($scope.additionalModelsData){
              _.extend(toSave, FieldTranslater.jsToPatient($scope.additionalModelsData));
            }

            $http.post('/api/v0.1/referral/' + $scope.route.slug + '/', toSave).then(
               function(response){
                  $scope.post_patient_text = null;
                  $scope.state = 'success';
                  $scope.success_link = response.data.success_link;
                  // clean out the additional model data
                  cleanAdditionalModelData();
                });
            };

        //
        // Return to the start of this referral route.
        //
        $scope.back = function(){
            $scope.state = 'initial';
            $scope.patient = null;
            $scope.hospital_number = null;
        };

    });
