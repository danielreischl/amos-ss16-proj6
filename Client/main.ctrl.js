/* This file should list all main controllers */

angular.module('app')

.controller("MainController", function(){
    var vm = this;
    vm.title = 'Welcome to the Main Page';
})

/* The side navigation should appear on button click */

.controller('sideNavController', function($scope, $mdSidenav) {
 $scope.openLeftMenu = function() {
        $mdSidenav('menue').toggle();
        };
})

/* controller for the graph example. This should show the files in the dropdown menue.
 The user is then able to chose from one, which will be displayed on the page*/


.controller('visuController', function($scope) {
    $scope.graphs = [
        {name : "Acceleration", file : "sections/graphExample/dummy.csv"},
        {name : "Power", file : "sections/graphExample/dummy2.csv"},
	];
    $scope.paintGraph = function(file) {
	    g2 = new Dygraph(
	    document.getElementById("graphdiv2"), file, {});
    }
})

/* Refresh the circle Page. The purporse of this controller is listen to the Button
 and upon receiving an event, it should trigger the update circle button*/


.controller('circleGraphController', function($scope, $compile, $mdDialog, $mdMedia) {

/* open up a dialogue window upon triggering it via button click */
    $scope.openDialog = function(carrier) {
    $mdDialog.show(
      $mdDialog.alert()
        .clickOutsideToClose(true)
        .title(carrier)
        .textContent('You can add this for comparison or take a closer look')
        .ok('Exit')
    );

    }

/* create the circle page upon button click. */

    $scope.circleGraph = function() {
    /*  first look if there are more carriers in the database than displayed right now.
    the functions looks for all divs with the class circle on it*/


  //TODO:  var x = document.querySelectorAll("div.circleDashboard");

    // create circle graphs and give them a unique ID

    var arrayCarrier = ["carrier1", "carrier2", "carrier3", "carrier4", "carrier5", "carrier6", "carrier7", "carrier8"];
    var arrayEnergy = [2, 42, 24, 10, 6, 4, 3, 23];
    var arrayAverageEnergy =[2, 30, 25, 11, 2, 7, 23, 87]
    var idCounter = 0;

    for (x in arrayCarrier) {


        var circleId = "carrier " + idCounter;
        var fragmenthtml = '<canvas class="circleDashboard" id="'+circleId+'" ng-click="openDialog(this.id)"></canvas>';
        var temp = $compile(fragmenthtml)($scope);
        angular.element(document.getElementById('circleGraphs')).append(temp);

        createCircle(circleId, arrayEnergy[idCounter], arrayAverageEnergy[idCounter]);
        idCounter = idCounter+1;
    }

    /*  This function will create the circle graph, depending on the input parameters from the databse (right now it is hard coded*/

    function createCircle(carrier, energy, averageEnergy) {

      var canvas = document.getElementById(carrier);
      var context = canvas.getContext('2d');
      var centerX = canvas.width / 2;
      var centerY = canvas.height / 2;
      var radius = 60;

      context.beginPath();
      context.arc(centerX, centerY, radius, 0, 2 * Math.PI, false);

      if( energy  > averageEnergy) {
         context.fillStyle = '#FF1744';
      } else if(energy  < averageEnergy ) {
             context.fillStyle = '#00BFA5';
      } else {
            context.fillStyle = "#FFFF8D";
      }

      context.fill();
      context.lineWidth = 5;
      context.lineWidth=1;
      context.fillStyle="#212121";
      context.lineStyle="#212121";
      context.font="15px sans-serif";
      context.fillText(carrier, centerX - 15, centerY);
    }


}})





