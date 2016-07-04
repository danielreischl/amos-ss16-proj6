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


/* This File is for modularizsation purposes. All new modules should be collected here.
*/

angular.module('app', ['ngRoute', 'app.routes', 'ngMaterial' , 'chart.js'])

/*
changing angularJS specific theme color, to our color set
*/

.config(function($mdThemingProvider) {

/*
create a ne color Ppalatte
*/
  $mdThemingProvider.definePalette('companyGreen', {
    '50': '#009688',
    '100': '#009688',
    '200': '#009688',
    '300': '#009688',
    '400': '#009688',
    '500': '#009688',
    '600': '#009688',
    '700': '#009688',
    '800': '#009688',
    '900': '#009688',
    'A100': '#009688',
    'A200': '#009688',
    'A400': '#009688',
    'A700': '#009688',
    'contrastDefaultColor': 'light',
    'contrastDarkColors': ['50', '100',
     '200', '300', '400', 'A100'],
    'contrastLightColors': undefined
 });

 /*
Use the color platte in combination with the default theme.
Only the accentPalatte will be changed to another color.
*/
  $mdThemingProvider.theme('default')
    .accentPalette('companyGreen');
});

