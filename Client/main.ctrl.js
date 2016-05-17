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
    $scope.dimensions = [
        {name : "Acceleration", id : "ACCELERATION", default: false},
        {name : "Energy", id : "ENERGY", default: false},
	{name : "Speed", id: "SPEED", default: false},
	{name : "Position", id: "POSITION", default: true},
    ];
    $scope.carriers = [
	{id : "1", name : "Carrier 1"},
	{id : "2", name : "Carrier 2"},
	{id : "3", name : "Carrier 3"},
    ];
    $scope.iterations = [
	{id : "1"},
	{id : "2"},
    ];
    $scope.selected =
	{ carrier: "1", iteration: "1" };
    $scope.paintGraph = function(file) {
	    g2 = new Dygraph(
	    document.getElementById("graphdiv2"), file, {});
        
         /*$scope.paintGraph = function(file) {
             g3 = new Dygraph(
                 document.getElementById("graphdiv3"), file, {});
         }
        */
    }
    $scope.paintGraphDynamic = function(carrier) {
	    g2 = new Dygraph(
	    document.getElementById("graphdiv2"), "django/helloWorld/position.csv?carrier="+$scope.selectedCarrier+"&iteration="+$scope.selectedIteration+"&dimension="+$scope.selectedDimension, {});
    }
})

/* controller for the compareGraph. Should display the comparison chart with all the carriers the user wants to compare*/

.controller('compareCircleGraph', function($scope, carrierService) {
    var carrierCompareList = carrierService.getCarrier();
    var carrierMax = 8; //this needs to be dynamic later if we have connection to the database
    var cool;
    var visibilityArray = [false, false, false, false, false, false, false, false, false, false]; //this needs to be dynamic later if we have connection to the database

    /* this functions created the dygraph  from a data source and applies options to them*/

    $scope.createCompareGraph = function() {
        graph = new Dygraph(
	       document.getElementById("compareGraph"), 'sections/compareCarrier/dummy.csv', {title: "Carrier's energy consumption of the latest iteration",
	                                                                                      ylabel: 'Energy Consumption in (mA)',
	                                                                                      xlabel: 'Time in (ms)',
	                                                                                      labelsSeparateLines: true,
	                                                                                      highlightSeriesOpts: {strokeWidth: 4, strokeBorderWidth: 1, highlightCircleSize: 5},
	                                                                                      visibility: visibilityArray,             // here are 10 x booleans because the dummy data has 3 extra commas
	                                                                                      });

        /* these loops have the purpose to see what carriers the user wants to compare
        and change the visibilty of the carriers in the dygraph to true */

        if(carrierCompareList.length != 0) {
            for (var i = 0; i < carrierCompareList.length; i++) {
                for (var carrier = 0; carrier < carrierMax; carrier++) {
                    if (carrierCompareList[i].carrierNumber == carrier) {
                        visibilityArray[carrier] = true;
                        break;
                    }
                }
            }
        } else {
            alert("You did not chose any Carriers to compare")
        }
    }
})

   

/* controller for the popupGraphs. Displays the carrier number and 2 Buttons. Depending on which button is pressed,
the carrier Id will be put into the comparison sidebar or the drill down chart*/

.controller('circlePopUpController', function($scope, $mdDialog, $mdSidenav, circleId, carrierService) {
    var id = circleId;
    var carrierId = id.substr(7, 8); // This method is necessary, because the string is "carrier_x" To extract x, I need to get the subsstring
    $scope.carrierNumber =  carrierId;

    $scope.addToComparison = function() {  //This function will add the carrier to the Side Panel "Compare". It will also check, if the item is already inside the comaprison pane.
        if(!carrierService.addCarrier(carrierId)) {         //check if carrier is already in list. If it already exists, then show a message.
            alert('Carrier: ' +carrierId+ ' is already in the comparison sidebar')
       }
        $mdDialog.hide();
        $mdSidenav('comparisonSidebar').toggle();
    }

    $scope.drillDown = function() {         //This function will take the carrier to the drilldown pane.
        alert("Moving to Drill Down Window, yet to be implemented");
        $mdDialog.hide();
    }
})

/* Refresh the circle Page. The purporse of this controller is listen to the Button
 and upon receiving an event, it should trigger the update circle button*/


.controller('circleGraphController', function($scope, $compile, $mdDialog, $mdMedia, $timeout, $mdSidenav, carrierService) {

/* open up a dialogue window upon triggering it via button click or via the hover function. The event is delayed by a timer
 if the the user is not leaving the hover area by the time the timer runs out, it will open up the popup. Else it will be canceled */
    var timer;

    $scope.openDialog = function(event) {
        var id = event.target.id;
        timer = $timeout(function () {
            $mdDialog.show({
                controller: "circlePopUpController",
                templateUrl: 'sections/circlePage/circlePopUp.html',
                clickOutsideToClose:true,
                locals: {circleId: id
                }
            });
        }, 1000)
    }

    $scope.closeDialog = function() {
        $timeout.cancel(timer);
    }


/* create the circle page upon page load. */

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
        context.fillText(carrier, centerX - 15, centerY); //carrier+1 to ensure right id for array and the right dosplay of carrier for the user
        context.fillText(percentageEnergy + "%", centerX - 15, centerY + 20);
    }
}

/* This function is for the side comparison navigation*/


    $scope.carriersForComparison = carrierService.getCarrier;

    $scope.removeCarrier = function(carrier) {
        carrierService.deleteCarrier(carrier);
    }

    $scope.openComparisonSideBar = function() {
        $mdSidenav('comparisonSidebar').toggle();
    }

})





