//
// Referr a patient
//
angular.module('opal.referral.controllers').controller(
    'ReferralCtrl', function($rootScope, $scope, $http,
                             focus, Episode, options,
                             referral_route, Item){
        $scope.route = referral_route;

        // Known states are:
        // Initial -> editing_demographics -> has_demographics -> success
        $scope.state = 'initial';
        $scope.hospital_number = null;
        $scope.patient = null;
        $scope.post_patient_text = null;
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
      	};


        $scope.lookup_hospital_number = function() {
            Episode.findByHospitalNumber(
                $scope.hospital_number,
                {
                    newPatient:    $scope.new_patient,
                    newForPatient: $scope.new_for_patient,
                    error        : function(){
                        // This shouldn't happen, but we should probably handle it better
                        alert('ERROR: More than one patient found with hospital number');
                    }
                });
        };

        $scope.new_patient = function(result){
            $scope.patient = {
                demographics: [{}]
            }
            $scope.state = 'editing_demographics';
            focus('input[name="patient_demographics[0]_name"]')
        };

        $scope.new_for_patient = function(patient){
            $scope.patient = patient;
            $scope.post_patient_text = 'We found ' + patient.demographics[0].name + " on the system. If that's not who you meant, you can enter your patient's details yourself."
            $scope.state   = 'has_demographics';
        }

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
            })

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
        }

        $scope.currentAdditionalData = function(){
            return _.find($scope.additionalModels, function(am){
                return am.name === $scope.state ;
            });
        }

        $scope.refer = function(){
            var demographics = _.clone($scope.patient.demographics[0]);
            if(demographics.date_of_birth){
                demographics.date_of_birth = moment(demographics.date_of_birth, 'DD/MM/YYYY').format('YYYY-MM-DD');
            }

            var postData = {
                 hospital_number: $scope.hospital_number,
                 demographics   : demographics
            };

            // additional model data is an object of model name -> populated model fields
            _.forEach($scope.additionalModelsData, function(item, key){
                  postData[key] = item.castToType(item);
            });

            $http.post('/api/v0.1/referral/' + $scope.route.slug + '/', postData).then(
               function(){
                  $scope.post_patient_text = null;
                  $scope.state = 'success';
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
            $scope.post_patient_text = null;
        }

    });
