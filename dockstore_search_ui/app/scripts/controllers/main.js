'use strict';

/**
 * @ngdoc function
 * @name dockstoreSearchUiApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the dockstoreSearchUiApp
 */

angular.module('dockstoreSearchUiApp')
    .controller('MainCtrl', function ($scope, $http) {
        $scope.info = "";
        $scope.search_query = {
            text: ""
        };
        var len_pre = 0

        $scope.change = function () {

            if($scope.search_query.text.length > 2 && $scope.search_query.text.length > len_pre) {
              $scope.info = $scope.search_query.text;

              $http({
                  method: "GET",
                  url: "http://127.0.0.1:5000/search_keywords=" + $scope.info,
                  data: {search_keywords : 'bri'}
              }).then(function mySucces(response) {
                  // $scope.myWelcome = JSON.parse(response.data);
                  console.log(response);
                  $scope.tools = response.data;
              }, function myError(response) {
                  $scope.tools = response.statusText;
              });
            }
            len_pre = $scope.search_query.text.length;
        };
    });
