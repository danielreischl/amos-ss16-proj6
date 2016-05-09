/* This file should list all main controllers */

angular.module('app')

.controller("MainController", function(){
    var vm = this;
    vm.title = 'Welcome to the Main Page';
})

.controller('sideNavController', sideNavController);
     function sideNavController ($scope, $mdSidenav) {
        $scope.openLeftMenu = function() {
        $mdSidenav('menue').toggle();
        };

     }
