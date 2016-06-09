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
  $scope.todos = ['Item 1', 'Item 2', 'Item 3'];
  $scope.addTodo = function () {
      $scope.todos.push($scope.todo);
      $scope.todo = '';
    };

//   $scope.students = [
//    {
//       "Name" : "Mahesh Parashar",
//       "RollNo" : 101,
//       "Percentage" : "80%"
//    },
//
//    {
//       "Name" : "Dinkar Kad",
//       "RollNo" : 201,
//       "Percentage" : "70%"
//    },
//
//    {
//       "Name" : "Robert",
//       "RollNo" : 191,
//       "Percentage" : "75%"
//    },
//
//    {
//       "Name" : "Julian Joe",
//       "RollNo" : 111,
//       "Percentage" : "77%"
//    }
// ];


              var my_url = "http://127.0.0.1:5000/search_keywords=bri";

              $http({
                  method : "GET",
                  url : "http://127.0.0.1:5000/search_keywords=bri"
              }).then(function mySucces(response) {
                  // $scope.myWelcome = JSON.parse(response.data);
                  console.log(response);
                  $scope.tools = response.data;
              }, function myError(response) {
                  $scope.tools = response.statusText;
              });

              $scope.info = "hello"

});
