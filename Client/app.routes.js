/* This File is for routing purposes. It should enable the one page view.
If the user clicks on a link to another html site, instead of loading the whole new webpage,
only a snippet will be loaded and sent to the index.html file.
*/


'use strict';

angular
    .module('app.routes', ['ngRoute'])

    .config(['$routeProvider', function($routeProvider) {
    $routeProvider

      .when('/Graph', {
        templateUrl: 'sections/graphExample/GraphExample.html',
      })

      .when('/Dashboard', {
        templateUrl: 'sections/dashboard/dashboard.html'
      })

      .otherwise({
        redirectTo: '/index.html',

       });
    }]);