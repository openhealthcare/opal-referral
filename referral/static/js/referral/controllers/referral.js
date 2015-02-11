//
// Referr a patient
//
angular.module('opal.referral.controllers').controller(
    'ReferralCtrl', function($rootScope, $scope, $http, 
                             focus,
                             Episode, options,
                             referral_route){
        $scope.route = referral_route;
        
        // Known states are:
        // Initial -> editing_demographics -> has_demographics -> success
        $scope.state = 'initial'; 
        $scope.hospital_number = null;
        $scope.patient = null;
        $scope.post_patient_text = null;

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

        $scope.refer = function(){
            var demographics = _.clone($scope.patient.demographics[0]);
            if(demographics.date_of_birth){
                demographics.date_of_birth = moment(demographics.date_of_birth, 'DD/MM/YYYY').format('YYYY-MM-DD')
            }
            $http.post('/referral/' + $scope.route.slug,
                       {
                           hospital_number: $scope.hospital_number, 
                           demographics   : demographics
                       }).then(
                           function(){
                               $scope.post_patient_text = null;
                               $scope.state = 'success';
                       })
        };
        
        // 
        // Return to the start of this referral route.
        // 
        $scope.back = function(){
            $scope.state = 'initial';
            $scope.patient = null;
        }

    });



