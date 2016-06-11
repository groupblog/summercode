'use strict';

/**
 * @ngdoc function
 * @name mySearchApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the mySearchApp
 */
angular.module('mySearchApp')
  .controller('MainCtrl', function ($scope, $http) {

  	$('table').sortable({items:'tr'});

  	$scope.search="";
  	$scope.change = function() {
  		if ($scope.search.length > 3){
	  		$http({
	  			method: "GET",
	  			url: "http://127.0.0.1:5000/data/"+$scope.search+"/",
	  			dataType: 'JSONP'
	  		}).then(function(response){
	  			$scope.searchs = response.data;
	  		});
  		}
  	};
  });
