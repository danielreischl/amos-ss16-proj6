/*
   This file is part of Rogue Vision.

   Copyright (C) 2016 Daniel Reischl, Rene Rathmann, Peter Tan,
       Tobias Dorsch, Shefali Shukla, Vignesh Govindarajulu,
       Aleksander Penew, Abinav Puri

   Rogue Vision is free software: you can redistribute it and/or modify
   it under the terms of the GNU Affero General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   Rogue Vision is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU Affero General Public License for more details.

   You should have received a copy of the GNU Affero General Public License
   along with Rogue Vision.  If not, see <http://www.gnu.org/licenses/>.
*/



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

      .when('/', {
        templateUrl: 'sections/barCirclePage/HomePageIcons.html'
      })

      .when('/CircleCarrier', {
        templateUrl: 'sections/circlePage/circleCarrier.html'
      })

      .when('/BarCarrier', {
        templateUrl: 'sections/barPage/Barchart.html'
      })
        
      .when('/CompareCarrier', {
        templateUrl: 'sections/compareCarrier/CompareCarrier.html'
      })

      .when('/AverageEnergyConsumptionChart', {
        templateUrl: 'sections/AverageEnergyConsumptionChart/AverageEnergyConsumptionChart.html'
      })

      .otherwise({
        redirectTo: '/',

       });
    }]);