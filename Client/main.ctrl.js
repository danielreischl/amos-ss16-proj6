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

/* controller for the popupGraphs. Displays the carrier number*/

.controller('circlePopUpController', function($scope) {
    $scope.title = "Carrier X, placeholder for the carrier ID";
})

/* Refresh the circle Page. The purporse of this controller is listen to the Button
 and upon receiving an event, it should trigger the update circle button*/


.controller('circleGraphController', function($scope, $compile, $mdDialog, $mdMedia, $timeout) {


/* open up a dialogue window upon triggering it via button click or via the hover function. The event is delayed by a timer
 if the the user is not leaving the hover area by the time the timer runs out, it will open up the popup. Else it will be canceled */
    var timer;

    $scope.openDialog = function(event) {
        timer = $timeout(function () {
            $mdDialog.show({
            controller: "circlePopUpController",
            templateUrl: 'sections/circlePage/circlePopUp.html',
            clickOutsideToClose:true
            })
        }, 1000)
    }

    $scope.closeDialog = function() {
        $timeout.cancel(timer);
    }


/* create the circle page upon button click. */

    $scope.circleGraph = function() {

    // create circle graphs and give them a unique ID

    var arrayCarrier = ["carrier1", "carrier2", "carrier3", "carrier4", "carrier5", "carrier6", "carrier7", "carrier8"];
    var arrayEnergy = [2, 42, 24, 10, 6, 4, 3, 23];
    var arrayAverageEnergy =[2, 30, 25, 11, 2, 7, 23, 87]
    var idCounter = 0;

    for (x in arrayCarrier) {

        var circleId = "carrier " + idCounter;
        var fragmenthtml = '<canvas class="circleDashboard" id="'+circleId+'" ng-click="openDialog($event)" ng-mouseenter="openDialog($event)" ng-mouseleave="closeDialog()"></canvas>';
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
      var percentageEnergy =  Math.round((energy/averageEnergy) * 100);

      context.beginPath();
      context.arc(centerX, centerY, radius, 0, 2 * Math.PI, false);
      context.lineWidth = 2;
      context.strokeStyle = '#003300';
      context.stroke();

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
      context.fillText(percentageEnergy + "%", centerX - 15, centerY + 20);
    }


}})





