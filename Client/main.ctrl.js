/* This file should list all main controllers */

angular.module('app')

.controller("MainController", function(){
    var vm = this;
    vm.title = 'Welcome to the Main Page';
})

.controller('sideNavController', function($scope, $mdSidenav) {
 $scope.openLeftMenu = function() {
        $mdSidenav('menue').toggle();
        };
})


.controller('visuController', function($scope) {
    $scope.graphs = [
        {name : "Acceleration", file : "sections/graphExample/dummy.csv"},
        {name : "Power", file : "sections/graphExample/dummy2.csv"},
	];
    $scope.paintGraph = function(file) {
	g2 = new Dygraph(
	    document.getElementById("graphdiv2"), file, {});
    }
});
