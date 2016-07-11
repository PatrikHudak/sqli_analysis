/* Main angular file */

'use strict';

var app = angular.module('App', []);

app.config(['$interpolateProvider', function($interpolateProvider) {
  $interpolateProvider.startSymbol('{[');
  $interpolateProvider.endSymbol(']}');
}]);

app.filter('humantime', function() {
  return function(input) {
    return moment.utc(input).calendar();
  };
});

app.filter('isotime', function() {
  return function(input) {
    return moment.utc(input).toISOString();
  };
});

app.controller('dashboard', ['$scope', '$http', function($scope, $http) {
  $http.get('/api/dashboard').success(function(data, status) {
    $scope.dashboard = data;
    $(function() {
      analysisActivity(data.analysis_graph);
    });
  });
}]);

app.controller('analysis', ['$scope', '$http', function($scope, $http) {
  $http.get('/api/analysis').success(function(data, status) {
    $scope.analyses = data.analyses;
  });
}]);

app.controller('canaries', ['$scope', '$http', function($scope, $http) {
  $scope.getCanaries = function() {
    $http.get('/api/canary').success(function(data, status) {
      $scope.canaries = data.canaries;
    });
  };

  $scope.createCanary = function() {
    $http.post('/api/canary').success(function(data, status) {
      $scope.created_canary = data.canary;
      $scope.getCanaries();
    });
  };

  $scope.deleteCanary = function(canary) {
    $http.post('/api/canary/' + canary).success(function(data, status) {
      $scope.created_canary = undefined;
      $scope.getCanaries();
    });
  }

  $scope.getCanaries();

}]);
