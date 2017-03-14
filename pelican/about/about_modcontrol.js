var a = angular.module("aboutApp", [], function($interpolateProvider) {
            $interpolateProvider.startSymbol('[[');
            $interpolateProvider.endSymbol(']]');
        }
    );

var datafactory = a.factory('datafactory', function($http, $q) {
    return {
        getNestData : function() {
            var deferred = $q.defer();
            var filename = 'about.json';
            $http.get(filename).success(function(data) {
                deferred.resolve(data);
            }).error(function(){
                console.log('error loading '+filename);
                deferred.reject();
            });
            return deferred.promise;
        }
    }
});

function PController($scope,datafactory) {
    $scope.initialize = function() {
        datafactory.getNestData().then(
            function(data) { 
                $scope.aboutData = data;
                console.log(data);
            }
        );
    }
}

// the first few arguments of the list should correspond to the Angular-namespace stuff to feed to HelloController
var c = a.controller("aboutController", ["$scope", "datafactory", PController]);

