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



/* This file should list all main controllers */
angular.module('app')

.controller("MainController", function(){
    var vm = this;
    vm.title = "Rogue Vision";
})

/* The side navigation should appear on button click */

.controller('sideNavController', function($scope, $mdSidenav) {
    // current state of the navigation. False means that the side navigation shows only the icons
    var state = false;

    /* Initializing butto ntext inside the navigation bar  */

    $scope.home = "";
    $scope.circleView = "";
    $scope.barView = "";
    $scope.alertView = "";
    $scope.simulation = "";
    $scope.settings = "";
    $scope.help = "";
    $scope.flexView ="";

    /* this scope will be triggered when the user wants to expand the navigation bar, The function inside will simply set the state to ture or false.
       and also the string inside the variables.
    */

    $scope.toggleSidebar = function() {
        if(state) {
            $scope.home = "";
            $scope.circleView = "";
            $scope.barView = "";
            $scope.alertView = "";
            $scope.simulation ="";
            $scope.settings = "";
            $scope.help = "";
            $scope.flexView = "";
            state = false;
        } else {
            $scope.home = "Home";
            $scope.circleView = "Circle Chart View";
            $scope.barView = "Bar Chart View";
            $scope.alertView = "Alert";
            $scope.simulation = "Simulation";
            $scope.settings = "Settings";
            $scope.help  = "Help";
            $scope.flexView = "Flexibility View";
            state = true;
        }
    }

    /* This scope will set the style, depending on the state variable. The style changes the width of the navigation sidebar */

    $scope.sideNavStyle = function() {
        var styleIcon = {"width": "50px", "height":"100%", "background-color": "#009688","overflow-x": "hidden" }
        var styleFull = {"width": "200px", "height":"100%", "background-color": "#009688"}

        if(state) {
            return styleFull;
        } else {
             return styleIcon;
        }

    }
})

/* controller for the compareGraph. Should display the comparison chart with all the carriers the user wants to compare*/
.controller('compareCircleGraph', function($scope, carrierService, $http, $window, percentageService, sessionService, iterationService) {

    // function that removes that the buttons are highlighted until you click somewhere else in the page
    $(".btn").mouseup(function(){
    $(this).blur();
    })

    // Switches Graph to requested View
    $scope.switchGraph = function(view){
        if (view=='AvgEng'){$window.location.href = '#AverageEnergyConsumptionChart';};
        if (view=='Circle'){$window.location.href = '#CircleCarrier';};
        if (view=='Spike'){$window.location.href = '#spikeContamination';};
        if (view=='Flexibility'){$window.location.href = '#flexibilityPage';};
    }


    // Get the array with the carriers that were selected from the carrierService
    var carrierCompareList = carrierService.getCarrier();

    // y-Axis labels for the dimensions
    var yAxisLabels = {'energyConsumption': 'Energy Consumption in W',
		       'positionAbsolute' : 'Position in mm',
		       'speed': 'Speed in m/s',
		       'acceleration': 'Acceleration in m/s*s',
		       'drive': 'Drive'};

    var units = {'energyConsumption': 'W',
		       'positionAbsolute' : 'mm',
		       'speed': 'm/s',
		       'acceleration': 'm/s*s',
		       'drive': 'Drive'};

    // make percentage service available in html-view
    // not very nice, try to refactor if possible
    $scope.percentageService = percentageService;
    $scope.sessionService = sessionService;

    // default value for the dimension and yAxislabel
    var selectedDimension = "energyConsumption"; // remove this later
    $scope.selectedDimension = "energyConsumption";
    var yAxisLabel = yAxisLabels[selectedDimension];

    $scope.selectedIteration = "";

     //Function that reads in the sessiondata json-file
    var sessionDataPromise = sessionService.getSessionData();
    sessionDataPromise.then(function(response){$scope.sessiondata = response.data});
    console.log("Simulation page says: " + JSON.stringify($scope.sessiondata));

    // if a iteration is Set, the iteration shouldn't be overwritten on initial call of controler
    if (iterationService.getIterations().length == 0){
        // default value for the selected Iterations
        var selectedIteration = "last"; // remove this later
        $scope.selectedIteration = "last";
    }

    var sessionDataPromise = sessionService.getSessionData();
    sessionDataPromise.then(function(response){$scope.sessions = response.data; console.log("Been here.");});
    console.log("main.ctrl.js says: " + JSON.stringify($scope.sessions));

    // the session requested from the database.
    $scope.currentSession = sessionService.getCurrentSession();

    //a string, which tells the database how many carrier the user is requesting.
    var carriersRequested = "";

    // Get the maxAmount of Carriers from the database and save it in a variable called amountOfCarriers
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", 'django/dataInterface/values.request?session='+$scope.currentSession+'&carrier=1&iteration=1&value=amountOfCarriers', false );
    xmlHttp.send(null);
    var amountOfCarriers = xmlHttp.responseText;

    // Get the last iteration database and save it
    var xmlHttp2 = new XMLHttpRequest();
    xmlHttp2.open( "GET", 'django/dataInterface/values.request?session='+$scope.currentSession+'&carrier=1&iteration=1&value=lastIteration', false );
    xmlHttp2.send(null);
    var amountOfIterations = xmlHttp2.responseText;

    //create an array depending on the amount of carriers. The items of the array will be used to initialize the checkboxes.
    $scope.carriers = [];
    updateCarrierArrayAndDrawGraph();

    //
    // Start of $scope
    //
    //Updates the current timestamp
    $scope.ts = new Date();

    $scope.dimensions = [
        {name : "Energy Consumption", id: 'energyConsumption'},
        {name : "Position", id: 'positionAbsolute'},
	{name : "Speed", id: 'speed'},
	{name : "Acceleration", id: 'acceleration'},
	{name : "drive", id : 'drive'},
    ]

    $scope.iterationDimensions = [
        {name : 'Last', id : 'last'},
	{name : 'Last 3', id : 'lastThree'},
        {name : "Last 10", id: 'lastTen'},
        {name : "All", id: 'all'}
    ]

    // Creates the dygraph from a data source and applies options to them
    $scope.createCompareGraph = function() {

	sessionService.setCurrentSession($scope.currentSession);

	//ensure that the variable is empty, before saving the new request path into it
        //var carriersRequested = "";

	    $scope.carriersRequested = function() {
	        // filter for the selected carriers
	        var selected = $scope.carriers.filter(function(carrier){return carrier.selected;});

	        //join them with commas
	        return selected.map(function(carrier){return carrier.id.toString();}).join();
	    }


         // Download file
         $scope.downloadFile = function(){
            window.location = $scope.requestedUrl;
           }

        // the url which should be requested will be defined in requestedUrl
        // to allow to export the csv file the variable is defined as a $scope variable
        $scope.requestedUrl = 'django/dataInterface/continuousData.csv?carriers='+ $scope.carriersRequested() + '&iterations=' + $scope.getSelectedIterationsString() + '&dimension=' + $scope.selectedDimension + '&session='+$scope.currentSession;

        graph = new Dygraph(
	        document.getElementById("compareGraph"),$scope.requestedUrl,
	            {title: yAxisLabels[$scope.selectedDimension],
	            ylabel: yAxisLabels[$scope.selectedDimension]+' in '+units[$scope.selectedDimension],
	            xlabel: 'time in ms',
	            labelsSeparateLines: true,
	            highlightSeriesOpts: {strokeWidth: 4, strokeBorderWidth: 1, highlightCircleSize: 5},
	            legend: "always",
	            showRangeSelector: true,
	            /*labelDiv looks for an element with the given id and puts the legend into this element.
	            Therefore the legend will not bis displayed inside the graph */
	            labelsDiv: document.getElementById("compareGraphLegend"),
	            axes: {
	                x: {
	                    /* formatting the x axis label in the legend. Now it will display not only the value but also a text */
	                    valueFormatter: function(x) {
                            return x + ' ms';
                        },
                        //Only draws axis with integers as labels
                        axisLabelFormatter: function(x) {
                            if(x % 1 == 0) {
            	                return x;
                            } else {
                                return "";
                            }
                        }
                    }
                },
	            });

        $scope.ts = new Date();
    }

    // gets percentageData from percentageService and fills carriers array with the selection and color information
    function updateCarrierArrayAndDrawGraph() {
	$scope.carriers.forEach(
	    function(carrier) {
		if (carrier.selected) {
		    carrierService.addCarrier(carrier.id);
		}
		else {
		    carrierService.deleteCarrier(carrier.id);
		}
	    });
	percentageService.getPercentagePromise().then(
	    function(result) {
		var percentageData = result.data;
		$scope.carriers = [];
		for (var idCounter = 1; idCounter <= Object.keys(percentageData).length; idCounter++) {
		    var currentSelected = carrierService.hasCarrier(idCounter);
		    $scope.carriers.push({id:idCounter, selected:currentSelected, color:percentageService.getColorOfCarrier(percentageData[idCounter])});
		}
		$scope.createCompareGraph();
	    });
    }

    $scope.getListStyle = function(index) {
        if (index % 5 == 1) {
                return {'clear': 'left'};
        }
        else {
                return {};
        }
    }

    $scope.updateFileName = function() {
	sessionService.setCurrentSession($scope.currentSession);
	$scope.currentFileName = sessionService.getDataFileNameById($scope.currentSession);
	updateCarrierArrayAndDrawGraph();
    }

    $scope.reload = function() {
	sessionService.setCurrentSession($scope.currentSession);
	$scope.currentFileName = sessionService.getDataFileNameById($scope.currentSession);
	updateCarrierArrayAndDrawGraph();
    }

    // This function empties the carriers in the comparison on page leave.
    // If the user leaves the current html snippet/template then,
    // this function will notice that and trigger the function "emptyCarrierArray" & emptyIterationArray
    $scope.$on("$destroy", function() {
        //carrierService.emptyCarrierArray();
        iterationService.emptyIterationArray();
    });

    //
    // Start of function
    //

    $scope.getSelectedIterationsString = function() {

        var selectedIterations = [];
        var selectedNumber;
        // TODO: add the possibility to select individual iterations
        switch ($scope.selectedIteration) {
        case "last":
             // Empties IterationArray
            iterationService.emptyIterationArray();
            selectedNumber = 1;
            break;
        case "lastThree":
             // Empties IterationArray
            iterationService.emptyIterationArray();
            selectedNumber = 3;
            break;
        case "lastTen":
            // Empties IterationArray
            iterationService.emptyIterationArray();
            selectedNumber = 10;
            break;
        case "all":
            // Empties IterationArray
            iterationService.emptyIterationArray();
            selectedNumber = amountOfIterations;
            break;
        default:
            selectedNumber = 0;
        }

        for (var i = amountOfIterations; i > amountOfIterations - selectedNumber && i >= 1; i--) {
            // Adds iteration to the iteration Service
            iterationService.addIteration(i);
        }
        // join with comma and return
        iterationReturn = iterationService.getIterations();
        // return comma seperated String with all requested iterations
        return iterationReturn.toString();
    }

})


/* controller for the AverageEnergyConsumption Chart. This chart will display the data over iterations. The user can select
which kind of data he wants to see. The default value is average energy consumption.*/
.controller('AverageEnergyConsumptionChart', function($scope, carrierService, percentageService, sessionService, $http, $window) {

    // function that removes that the buttons are highlighted until you click somewhere else in the page
    $(".btn").mouseup(function(){
    $(this).blur();
    })

    // get the array with the carriers the user wants to see in the graph.
    var carrierCompareList = carrierService.getCarrier();

    // y-Axis labels for different dimensions
    var yAxisLabels = {'energyConsumptionAverage' : 'Average Energy Consumption',
		       'accelerationAverage' : 'Average Acceleration',
		       'speedAverage': 'Average Speed',
		       'energyConsumptionTotal': 'Total Energy Consumption' };

    var units = {'energyConsumptionAverage': 'W',
		 'accelerationAverage' : '?',
		 'speedAverage': 'mm/ms',
		 'energyConsumptionTotal': 'W' };

    // Sets the initial time for the time stamp
    $scope.ts = new Date();

    // default value for the dimension and yAxislabel
    $scope.selectedDimension = "energyConsumptionTotal";

    $scope.selectedIteration = "last10";

     //Function that reads in the sessiondata json-file
    var sessionDataPromise = sessionService.getSessionData();
    sessionDataPromise.then(function(response){$scope.sessiondata = response.data});
    console.log("Simulation page says: " + JSON.stringify($scope.sessiondata));


    // the session requested from the database.
    $scope.currentSession = sessionService.getCurrentSession();

    //a string, which tells the database how many carrier the user is requesting.
    var carriersRequested = "";

    // Get the maxAmount of Carriers from the database and save it in a variable called amountOfCarriers
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", 'django/dataInterface/values.request?session='+$scope.currentSession+'&carrier=1&iteration=1&value=amountOfCarriers', false );
    xmlHttp.send(null);
    var amountOfCarriers = xmlHttp.responseText;

    //create an array depending on the amount of carriers. The items of the array will be used to initialize the checkboxes.
    $scope.carriers = [];
    updateCarrierArrayAndDrawGraph();

    // create the dropdown menu for iterations. the id is corresponding to the key word used in the database to extract the dimension.
    $scope.iterationDimensions = [
        {name : "Last 10 Iterations", id : 'last10'},
        {name : "All Iterations", id : 'all'}
    ]

    // create the dropdown menu for dimensions. the id is corresponding to the key word used in the database to extract the dimension.
    $scope.dimensions = [
        {name : "Average Energy Consumption", id : 'energyConsumptionAverage'},
        {name : "Average Acceleration", id : 'accelerationAverage'},
	    {name : "Average Speed", id: 'speedAverage'},
	    {name : "Total Energy Consumption", id: 'energyConsumptionTotal'}
    ]

    // make percentage service available in html-view
    // not very nice, try to refactor if possible
    $scope.percentageService = percentageService;

    // Switches Graph to requested View
    $scope.switchGraph = function(view){
        if (view=='ContEng'){$window.location.href = '#CompareCarrier';};
        if (view=='Circle'){$window.location.href = '#CircleCarrier';};
        if (view=='Spike'){$window.location.href = '#spikeContamination';};
        if (view=='Flexibility'){$window.location.href = '#flexibilityPage';};

    }

    // gets percentageData from percentageService and fills carriers array with the selection and color information
    function updateCarrierArrayAndDrawGraph() {
	$scope.carriers.forEach(
	    function(carrier) {
		if (carrier.selected) {
		    carrierService.addCarrier(carrier.id);
		}
		else {
		    carrierService.deleteCarrier(carrier.id);
		}
	    });
	percentageService.getPercentagePromise().then(
	    function(result) {
		var percentageData = result.data;
		$scope.carriers = [];
		for (var idCounter = 1; idCounter <= Object.keys(percentageData).length; idCounter++) {
		    var currentSelected = carrierService.hasCarrier(idCounter);
		    $scope.carriers.push({id:idCounter, selected:currentSelected, color:percentageService.getColorOfCarrier(percentageData[idCounter])});
		}
		$scope.createAverageEnergyConsumptionChart();
	    });
    }

    $scope.reload = function() {
	sessionService.setCurrentSession($scope.currentSession);
	$scope.currentFileName = sessionService.getDataFileNameById($scope.currentSession);
	updateCarrierArrayAndDrawGraph();
    }

     // This function receives the changes from the dropDown menu "dimensions" and changes the yAxis name of the graph and requests the needed data by changing the string name.
    // $scope.changeDimension = function() {
    //	    selectedDimension = $scope.selectedDimension;
    //	 }

    /* this functions creates the dygraph  from a data source and applies options to them*/

    $scope.createAverageEnergyConsumptionChart = function() {

	$scope.carriersRequested = function() {
	    // filter for the selected carriers
	    var selected = $scope.carriers.filter(function(carrier){return carrier.selected;});

	    //join them with commas
	    return selected.map(function(carrier){return carrier.id.toString();}).join();
	}


	sessionService.setCurrentSession($scope.currentSession);
	$scope.currentSession = sessionService.getCurrentSession();

        // create the graph with the parameters set. The request path for the database depends on 3 parameters: session, carrierRequested, selectedDimension and type
        // the url which should be requested wil be defined in requestedUrl
        // to allow to export the csv file the variable is defined as a $scope variable
        $scope.requestedUrl = 'django/dataInterface/averageEnergyConsumption.csv?session='+$scope.currentSession+'&carriers='+$scope.carriersRequested()+'&dimension='+$scope.selectedDimension+'&type='+$scope.selectedIteration;



         // Download file
         $scope.downloadFile = function(){
            window.location = $scope.requestedUrl;
            }

        graph = new Dygraph(
	       document.getElementById("AverageEnergyConsumptionChart"),$scope.requestedUrl ,
	                                                                                     {title: yAxisLabels[$scope.selectedDimension],
	                                                                                      ylabel: yAxisLabels[$scope.selectedDimension]+' in '+units[$scope.selectedDimension],
	                                                                                      xlabel: 'Iteration',
	                                                                                      labelsSeparateLines: true,
	                                                                                      highlightSeriesOpts: {strokeWidth: 4, strokeBorderWidth: 1, highlightCircleSize: 5},
	                                                                                      legend: "always",
	                                                                                      /*labelDiv looks for an element with the given id and puts the legend into this element.
	                                                                                       Therefore the legend will not bis displayed inside the graph */
	                                                                                      labelsDiv: document.getElementById("compareAverageEnergyConsumptionGraphLegend"),
	                                                                                      axes: {
                                                                                            x: {
                                                                                                /* formatting the x axis label in the legend. Now it will display not only the value but also a text */
                                                                                                valueFormatter: function(x) {
                                                                                                    return 'Iteration ' + x;
                                                                                                },
                                                                                                // Only draws axis with integers as labels
                                                                                                axisLabelFormatter: function(x) {
                                                                                                  if (x % 1 == 0) {
                                                                                                    return x;
                                                                                                  } else {
                                                                                                    return "";
                                                                                                  }
                                                                                                }
                                                                                              }
                                                                                          },
	                                                                                      });



	$scope.getListStyle = function(index) {
	    if (index % 5 == 1) {
		    return {'clear': 'left'};
	    }
	    else {
		    return {};
	    }
	}

	$scope.updateFileName = function() {
	    $scope.currentFileName = sessionService.getCurrentDataFileName($scope.currentSession);
	}

        // Updates the  time for the time stamp
        $scope.ts = new Date();
    }
})


/* Refresh the circle Page. The purpose of this controller is listen to the Button
 and upon receiving an event, it should trigger the update circle button*/
.controller('circleGraphController', function($scope, $compile, $mdDialog, $mdMedia, $timeout, $http, $mdSidenav, carrierService, percentageService, sessionService) {
    // title and button will change, depending on which circleView is showing.
    var changed = 0;
    $scope.circleView_title = "Creeping Contamination";
    $scope.circleView_button = "Continuous Contamination";

    // data variable to be changed
    var percentageDataType = "percentages_creeping";

    // sets the current File Name
    $http.get("django/dataInterface/rawData.json?table=sessiondata").then(function (response){
        $scope.currentFileName = response.data[sessionService.getCurrentSession()-1].fields.fileName;
        $scope.fileStatus = response.data[sessionService.getCurrentSession()-1].fields.status;
    });
    /* Button, changes the title of the view and the data displayed. It will also redraw the circles with the new data */
    $scope.changeView = function() {
       if(changed == 0) {
           clearCanvas();
           percentageDataType = "percentages_cont";
	   percentageService.setPercentageType(percentageDataType);
           $scope.circleView_title = "Continuous Contamination";
           $scope.circleView_button = "Creeping Contamination";
           changed = 1;
       } else {
           clearCanvas();
           percentageDataType = "percentages_creeping";
	   percentageService.setPercentageType(percentageDataType);
           $scope.circleView_title = "Creeping Contamination";
           $scope.circleView_button = "Continuous Contamination";
           changed = 0;
       }
        $scope.circleGraph();
    }

    // Initializes time stamp
    $scope.ts = new Date();
    /* This function will highlight the carrier and save the id of the carrier inside the comparison array in app.service.js*/
    $scope.selectCarrier = function(event) {
        // id = carrier x
        var id = event.target.id;

        // This method is necessary, because the string is "carrier x" To extract the int x, the substring is needed
        var carrierId = parseInt(id.substr(7, 8));

        //check if carrier is already in list.
        if(!carrierService.addCarrier(carrierId)) {
            //Already in the list, remove the highlight
            drawSelectionOnCarrier(carrierId, false);

            //If it exists delete the carrier
            carrierService.deleteCarrier(carrierId);
        } else {
            //Not in the list, highlight
            drawSelectionOnCarrier(carrierId, true);
        }
    }

    function redrawAllSelections() {
        for(var i = percentageService.getAll().length; i >= 1; i--) {
            var hasCarrier = carrierService.containsCarrier(i);
            if (hasCarrier) {
                drawSelectionOnCarrier(i, true);
            }
        }
    }

    // Draws or removes selection circle around given canvas context for id (integer)
    // if selection is true it draws the selection on the carrier
    // If selection is false it removes the selection on the carrier
    function drawSelectionOnCarrier(id, selection) {
        var canvas = document.getElementById("carrier " + id);
        if (canvas == null) {
            return;
        }
        var context = canvas.getContext('2d');
        var centerX = canvas.width / 2;
        var centerY = canvas.height / 2;
        var radius = 70;

        context.beginPath();
        context.arc(centerX, centerY, radius, 0, 2 * Math.PI);
        if (selection) {
            context.lineWidth = 7;
            context.strokeStyle = "#003300";
        } else {
            context.lineWidth = 9;
            context.strokeStyle = "#ECEFF1";
        }
        context.stroke();
    }

     //* this function will clear the drawn canvas and enables redraw functions to draw on a new canvas */
    function clearCanvas() {
        // delete all canvas elements, previously created for all carriers
        var parent = document.getElementById("circleGraphs");
            while (parent.firstChild) {
                parent.removeChild(parent.firstChild);
            }
    }

    $scope.refresh = function() {
        //clear circle canvas elements
        clearCanvas()
        // Redraw circles
        $scope.circleGraph();
        // Redraw selection
        redrawAllSelections();
        //Update the timestamp
        $scope.ts = new Date();
        // sets the current File Name
        $http.get("django/dataInterface/rawData.json?table=sessiondata").then(function (response){
            $scope.currentFileName = response.data[sessionService.getCurrentSession()-1].fields.fileName;
            $scope.fileStatus = response.data[sessionService.getCurrentSession()-1].fields.status;
        });
    }


    /*
     *  get percentage data from service
     *  after data arrived call the functoin circleGraphMain that acutally paints the circles
    */
    $scope.circleGraph = function () {
	percentageService.getPercentagePromise()
	    .then(function(result){$scope.circleGraphMain(result.data)});
    }

    /* create the circle page upon page load. */
    $scope.circleGraphMain = function(carrierPercentageData) {

        console.log(carrierPercentageData);
        var amountOfCarriers = Object.keys(carrierPercentageData).length;

        /* ID of first Carrier */
        var idCounter = 1;

        //delay the creation of the circles by 0 second, so that the percentage data can be loaded into the function.
        createCarrierHTML();

        // function to create HTML circle fragments dynamically
        function createCarrierHTML() {

            /* for every carrier in the database, create a new code fragment to be injected into the html file. Each fragment is the base for a circle */
	    console.log("createCarrierHTML");
            while (amountOfCarriers > 0) {
                var circleId = "carrier " + idCounter;
                var fragmenthtml = '<canvas class="circleDashboard" id="'+circleId+'" ng-click="selectCarrier($event)"></canvas>';
                var temp = $compile(fragmenthtml)($scope);
                var hasCarrier = carrierService.containsCarrier(idCounter);


                // get the element in the html page, on which the new fragment should be appended to
                angular.element(document.getElementById('circleGraphs')).append(temp);
                // call the circle drawing method to paint the circles. It will get the ID of the carrier, as well as the percentage data
                createCircle(circleId, carrierPercentageData[idCounter]);

                // If the carrier is in the selection then draw the selection circle
                if (hasCarrier) {
                    drawSelectionOnCarrier(idCounter, true);
                }

                idCounter = idCounter+1;
                amountOfCarriers = amountOfCarriers -1;
            }
        }

        /*  This function will create the circles, depending on the input parameters from the database*/
        function createCircle(carrier, percentageOfEnergy) {
            var canvas = document.getElementById(carrier);
            var context = canvas.getContext('2d');
            var centerX = canvas.width / 2;
            var centerY = canvas.height / 2;
            var radius = 60;

            context.beginPath();
            context.arc(centerX, centerY, radius, 0, 2 * Math.PI, false);
            context.lineWidth = 2;
            context.strokeStyle = '#003300';
            context.stroke();

            /* Logic of the color: if the percentage of a carrier is above 1.05 it will be coded red,
               because the energy consumption of the last iteration is too high in comparison to the
               first iteration. If the value is < 1.025, then the color will be green, because the energy
               consumption is not really increasing much.
               Any value between is coded yellow, because it should warn the user, that the energy
               is higher than the very first iteration.
             */
            if(percentageOfEnergy > 1.05) {
                context.fillStyle = '#e51c34';
            } else if(percentageOfEnergy <= 1.025 ) {
                context.fillStyle = '#b2ff59';
            } else {
                context.fillStyle = "#ffff00";
            }

            context.fill();
            context.lineWidth = 5;
            context.lineWidth = 1;
            context.fillStyle = "#212121";
            context.lineStyle = "#212121";
            context.font = "15px sans-serif";
            // textAlign center will allign the text relative to the borders of the canvas
            context.textAlign = 'center';
            context.fillText(carrier, centerX, centerY - 7);
            context.fillText((percentageOfEnergy*100).toFixed() + "%", centerX, centerY + 12);
        }
    }
})

.controller('sessionDataTable', function($scope, $http) {
    $http.get("django/dataInterface/rawData.json?table=sessiondata")
    .then(function (response) {$scope.names = response.data.records;});
})

/* bar chart View controller */

.controller('barGraphController',function($scope, $timeout, $http, carrierService, percentageService, sessionService) {

    $scope.ts = new Date();

    $scope.refresh = function() {
        // Redraw bar chart view
        $scope.barGraph();
        // Update the timestamp
        $scope.ts = new Date();
    }

    $scope.barGraph = function() {

        // get the data from the percentage service and save it into the variables, carrierPercentageData and amountOfCarriers
        var percentageDataType = "percentages_creeping";
	percentageService.setPercentageType(percentageDataType);
        //var carrierPercentageData = percentageService.getAll(percentageDataType);

        // this array saves the percentage of each bar column/carrier
        var carrierPercentageDataRounded = [];
        // this array saves the color of each bar column/carrier
        var carrierColorArray = [];
        // this array saves the names of each bar column/carrier
        //var carrierArray = [];
        /* ID of first Carrier */
        var idCounter = 1;

         // sets the current File Name
          $http.get("django/dataInterface/rawData.json?table=sessiondata").then(function (response){$scope.currentFileName = response.data[sessionService.getCurrentSession()-1].fields.fileName;});

        // timer is set to 1.6 second. this wait time is needed to fetch all data from the database
        //$timeout(createBarChartView, 0);

	//function createBarCharView() {
	var carrierPercentageDataPromise = percentageService.getPercentagePromise();
	carrierPercentageDataPromise.then(
	    function(result){createBarChartViewMain(result.data)}
	);
	//}

	var createBarChartViewMain = function(carrierPercentageData) {
            // This while loop will fill the carrierArray with carrier names for the chart label
	    var amountOfCarriers = Object.keys(carrierPercentageData).length;
	    var carrierArray = Object.keys(carrierPercentageData);
	    console.log(carrierPercentageData);
	    console.log(carrierArray);
            //while (amountOfCarriers > 0) {
            //    carrierArray.push("carrier " + idCounter)
            //    idCounter = idCounter+1;
            //    amountOfCarriers = amountOfCarriers -1;
            //}

            /*  This for loop will round the percentage data and save it into a new array.
                It will also fill the color array with the color, corresponding to the percentage of
                the carrier. E.g. green is up to 102,5% , yellow is up 102,5 to 105% and everything above is red
            */
            for(var carrier = 1; carrier <= amountOfCarriers; carrier++) {
		console.log(carrier);
                if(carrierPercentageData[carrier] > 1.05) {
                    carrierColorArray.push('rgba(229, 28, 52, 1)')
                    carrierPercentageDataRounded.push((carrierPercentageData[carrier]*100).toFixed())
                } else if(carrierPercentageData[carrier] <= 1.025 ) {
                    carrierColorArray.push('rgba(178, 255, 89, 1)')
                    carrierPercentageDataRounded.push((carrierPercentageData[carrier]*100).toFixed())
                } else {
                    carrierColorArray.push('rgba(255,255,0, 1)')
                    carrierPercentageDataRounded.push((carrierPercentageData[carrier]*100).toFixed())
                }
            }
	    console.log(carrierColorArray);
	    console.log(carrierPercentageDataRounded);

            /*  get the element where the bar chart should be displayed and
                create the chart with different parameters.
            */
            var ctx = document.getElementById("barChart").getContext("2d");
            ctx.canvas.width = 800;
            ctx.canvas.height = 600;

            var myChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: carrierArray,
                        datasets: [{
                            label: 'Energy Consumption in %',
                            data: carrierPercentageDataRounded,
                            backgroundColor: carrierColorArray,
                            borderColor: 'rgba(31,27,28, 1)',
                            borderWidth: 1,
                        }]
                },
                options: {
                    scales: {
                        yAxes: [{
                            ticks: {
                                beginAtZero:true
                            }
                        }]
                    },
                }
            });
        }
    }

})

// Controller that contains all function for the spikeContamination page
.controller('spikeContaminationController', function($scope, $http, sessionService, carrierService, iterationService, $window) {

    // sets current time for timestamp
     $scope.ts = new Date();


     $scope.refresh = function() {
        // Update the timestamp
        $scope.ts = new Date();
        // Calls updatedata
        $scope.updatedata
    }

    // gets current session
    session = sessionService.getCurrentSession();

    // function that updates all data
    $scope.updatedata = function(){
    // gets SpikeData
    $http.get("django/dataInterface/spikeContamination.json?session=" + session)
    .then(function (response){$scope.spikedata = response.data;});

    // sets the current File Name
    $http.get("django/dataInterface/rawData.json?table=sessiondata").then(function (response){
    console.log ("Getting Json File")
    $scope.currentFileName = response.data[sessionService.getCurrentSession()-1].fields.fileName;
    });

    // sets Values and redirects to continuesGraph
    $scope.setValues = function(carrier, iteration){
        console.log("SetValues started.");
        // Sets Carrier to selected Carrier
        carrierService.emptyCarrierArray();
        carrierService.addCarrier(carrier);
        // Sets Iteration to selected Iteration
        iterationService.emptyIterationArray();
        iterationService.addIteration(iteration);
        // Redirects to Cont Graph
        $window.location.href = '#CompareCarrier';

    };
    }
})

.controller('simulationPageController', function($scope, $http, $window, sessionService) {

    $http.get("django/dataInterface/simulation.running").then(function (response){
        if (response.data == "True"){
            $scope.running = true;
        }else{
            $scope.running = false;
        }
    });

    // This saves all Data File Names that are stored on the server
    $scope.dataFileNames = getArrayOfDataFiles();

    // Standard Values
    $scope.amountOfCarriers = 15;
    $scope.waitForCompression = 0;
    $scope.waitForFirstDataLoad = 30;
    $scope.waitForDataReload = 30;
    $scope.keepEveryXRows = 100;

    //Function that reads in the sessiondata json-file
    var sessionDataPromise = sessionService.getSessionData();
    sessionDataPromise.then(function(response){$scope.sessiondata = response.data});
    console.log("Simulation page says: " + JSON.stringify($scope.sessiondata));

    //Starts the simulation by calling the website link
    $scope.startSimulation = function() {
            var urlString = 'django/dataInterface/simulation.start?wtSimulation=' + $scope.waitForCompression + '&wtFirstDataload=' + $scope.waitForFirstDataLoad + '&wtDataReload=' + $scope.waitForDataReload + '&amountOfCarriers=' + $scope.amountOfCarriers + '&fileName=InitialData/' + $scope.selectedDataFile  + '&keepEveryXRows=' + $scope.keepEveryXRows
            xmlHttp = new XMLHttpRequest();
            xmlHttp.open( "GET", urlString, false);
            xmlHttp.send(null);
            var returnString  = xmlHttp.responseText;
            //Sets the current Session to the new SessionNumber
            sessionService.setCurrentSession(parseInt(sessionService.getNumberOfSessions())+1);
            alert("Simulation Started");
            //refreshes the website
            $window.location.href = '#simulation';

    };

    // Calls URL to reset the Sytem and prompts an alert
    $scope.resetSimulation = function(){
    $http.get("django/dataInterface/simulation.reset")
    .then(function(response){alert ('System reseted');});
    };

    // Function that sets the currentSession to submittedSession and redirects to the Circle Vuew
    $scope.setSession = function(submittedSession){
        sessionService.setCurrentSession(submittedSession)
        // Redirects to Circle View
        $window.location.href = '#CircleCarrier';
    }

    $scope.uploadFile = function() {
	var formData = new FormData(document.forms.namedItem("fileUpload"));
	var xhr = new XMLHttpRequest();
	xhr.upload.addEventListener("progress", uploadProgress,false);
	xhr.addEventListener("load", uploadComplete,false);
	xhr.addEventListener("error", uploadFailed,false);
	xhr.open("POST","django/dataInterface/fileUpload.html");
	xhr.send(formData);
    }

    function uploadComplete(event) {
	$scope.dataFileNames = getArrayOfDataFiles();
	alert(event.target.responseText);
	//$scope.progress = 'completed';
    }

    function uploadFailed(event) {
	alert('The upload failed.');
	$scope.progress = "The upload failed.";
    }

    function uploadProgress(event) {
	$scope.$apply(function() {
	    if(event.lengthComputable) {
		$scope.progress = Math.round(event.loaded * 100 / event.total);
	    }
	    else {
		$scope.progress = "Process could not be computed.";
	    }
	});
    }

    // This gets all Data File Names that are stored on the server
    function getArrayOfDataFiles() {

        // Gets the full string of all datapaths of all data files on the server
        var xmlHttp = new XMLHttpRequest();
        xmlHttp.open( "GET", 'django/dataInterface/simulation.files', false);
        xmlHttp.send(null);
        var string  = xmlHttp.responseText;

        // Separates the comma seperated data files string to an array
        var arraySimulationFileNames = string.split(',');

        // Deletes the file path for every file name so that only the file name is displayed
        for (var i = 0; i < arraySimulationFileNames.length; i++) {
            arraySimulationFileNames[i] = arraySimulationFileNames[i].substring(32);
        }

        // returns an array with all FileNames
        return arraySimulationFileNames;

    }
})

/* controller for the Flexibility Chart. This chart will display the speed data of each carrier over absolute time. The user can select
the session, iterations and carriers he wans to see. */
.controller('FlexibilityChartController', function($scope, $http, $window, carrierService, percentageService, sessionService) {

    // function that removes that the buttons are highlighted until you click somewhere else in the page
    $(".btn").mouseup(function(){
    $(this).blur();
    })

    // get the array with the carriers the user wants to see in the graph.
    var carrierCompareList = carrierService.getCarrier();

    // Sets the initial time for the time stamp
    $scope.ts = new Date();

    //Function that reads in the sessiondata json-file
    var sessionDataPromise = sessionService.getSessionData();
    sessionDataPromise.then(function(response){$scope.sessiondata = response.data});
    console.log("Simulation page says: " + JSON.stringify($scope.sessiondata));

    // the session requested from the database.
    $scope.currentSession = sessionService.getCurrentSession();

    //a string, which tells the database how many carrier the user is requesting.
    var carriersRequested = "";

    // Get the maxAmount of Carriers from the database and save it in a variable called amountOfCarriers
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", 'django/dataInterface/values.request?session='+$scope.currentSession+'&carrier=1&iteration=1&value=amountOfCarriers', false );
    xmlHttp.send(null);
    var amountOfCarriers = xmlHttp.responseText;

    // Get the last iteration database and save it
    var xmlHttp2 = new XMLHttpRequest();
    xmlHttp2.open( "GET", 'django/dataInterface/values.request?session='+$scope.currentSession+'&carrier=1&iteration=1&value=lastIteration', false );
    xmlHttp2.send(null);
    var lastIteration = xmlHttp2.responseText;

    //create an array depending on the amount of carriers. The items of the array will be used to initialize the checkboxes.
    $scope.carriers = [];
    //updateCarrierArrayAndDrawGraph();

    // create the dropdown menu for iterations. the array gets filled with the iteration numbers available in the database.
    $scope.iterations = [];
    for (var i = 1; i <= lastIteration;i++) {
	    $scope.iterations.push(i);
    }

    //set the first iterations to default.
    $scope.selectedIteration = $scope.iterations[0];

    // make percentage service available in html-view
    // not very nice, try to refactor if possible
    $scope.percentageService = percentageService;

     // Switches Graph to requested View
    $scope.switchGraph = function(view){
        if (view=='ContEng'){$window.location.href = '#CompareCarrier';};
        if (view=='Circle'){$window.location.href = '#CircleCarrier';};
        if (view=='Spike'){$window.location.href = '#spikeContamination';};
    }

    // Get selected carriers
    $scope.carriersRequested = function() {
            // filter for the selected carriers
            var selected = $scope.carriers.filter(function(carrier){return carrier.selected;});

            //join them with commas
            return selected.map(function(carrier){return carrier.id.toString();}).join();
    }
    // flexibility measure
    $scope.flexibilityMeasure = calculateFlexibilityMeasure();

    // returns the flexibility measure
    function calculateFlexibilityMeasure() {

        // Get the last iteration database and save it
        var xmlHttp3 = new XMLHttpRequest();
        var requestURLString = 'django/dataInterface/continuousDataAbsoluteTime.csv?carriers='+$scope.carriersRequested()+'&iterations='+$scope.selectedIteration+'&dimension=speed&session='+$scope.currentSession;
        xmlHttp3.open( "GET", requestURLString, false);
        xmlHttp3.send(null);
        var flexString = xmlHttp3.responseText;

        // Transform the raw csv file into a 2d array
        var flexibilityArray = splitCSVToArray(flexString);

        // Calculate the flexibility measure from the 2d array
        var measure = calculateFlexibilityMeasure(flexibilityArray);

        // Splits the absolute time csv file into different rows for every new line
        // and then into different columns for every ","
        function splitCSVToArray(string) {
            // Splits the string array for every new line
            var lineArray = string.split('\n');

            // Goes through the new line array and splits the array up for every comma
            for (var i = 0; i < lineArray.length; i++) {
                lineArray[i] = lineArray[i].split(',');

                // Parses to int (and NaN in the case of no value)
                for (var j = 0; j < lineArray[i].length; j++) {
                    lineArray[i][j] = parseFloat(lineArray[i][j])
                }
            }

            return lineArray;
        }

        // Takes a 2d array with one header, new line ("\n") for row and "," for column and calculates the flexibility
        // measure
        function calculateFlexibilityMeasure(array) {
            // The sum of all deviations from the mean over all rows
            var sumOfMeasures = 0.0;
            // the amount of rows that had more than 1 values
            var amountOfMeasures = 0;

            // Iterate through all rows (timestamps)
            for (var i = 1; i < array.length; i++) {
                // Sum of values for calculating the mean in that row
                var sumOfNumbers = 0.0;
                // Amount of numbers in that row
                var amountOfNumbers = 0;

                // Iterate through all columns for that row (all carriers speed during that timestamp)
                for (var j = 1; j < array[i].length; j++) {
                    // console.log("array["+i+"]["+j+"]: " + array[i][j]);

                    // Checks if data entry has a number
                    if (isNaN(array[i][j]) == false) {
                        // Add data entry to sum for calculating the mean
                        sumOfNumbers += array[i][j];
                        amountOfNumbers += 1;
                    }
                }
                // console.log("finished i: " + i + " with " + amountOfNumbers + " numbers");

                // If more than one data point in that row (more than one carrier is moving during that time)
                // then the flexibility measure for that timestamp can be calculated
                if (amountOfNumbers > 1) {
                    // Calculate the mean for that row
                    var middle = 0.0;
                    middle = (sumOfNumbers/amountOfNumbers);

                    // Calculate the average deviation from the mean for every column in that row
                    var totDeviation = 0.0;
                    for (var j = 1; j < array[i].length; j++) {
                        if (isNaN(array[i][j]) == false) {
                            var deviation = 0.0;
                            if (array[i][j] > middle) {
                                deviation = Math.abs(array[i][j] - middle);
                            } else {
                                deviation = Math.abs(middle - array[i][j]);
                            }
                            totDeviation += deviation;
                        }
                    }
                    // add the deviation to the sum of deviations
                    sumOfMeasures += (totDeviation/amountOfNumbers);
                    amountOfMeasures += 1;
                    // console.log("new AMes (" + amountOfMeasures + ") SMes: " + sumOfMeasures + " = totDEV: " + totDeviation + " / AONum: " + amountOfNumbers);

                }
            }
            // If no rows with multiple carriers have been found, return 0 to avoid dividing by 0
            if (amountOfMeasures == 0) {
                return 0;
            }
            // Divide the sumOfMeasures by amountOfMeasures to get the average deviation for all timestamps
            var finalMeasure = (sumOfMeasures/amountOfMeasures);
            // Takes Measure times 100 and rounds it to last 2 decimals
            // Converts 0,0333333 to 3,33
            finalMeasure = (Math.round(finalMeasure * 10000)) / 100;
            return finalMeasure;
        }

        return measure;
    }

    function updateCarrierArrayAndDrawGraph(init) {
	$scope.carriers.forEach(
	    function(carrier) {
		if (carrier.selected) {
		    carrierService.addCarrier(carrier.id);
		}
		else {
		    carrierService.deleteCarrier(carrier.id);
		}
	    });
	percentageService.getPercentagePromise().then(
	    function(result) {
		var percentageData = result.data;
		$scope.carriers = [];
		for (var idCounter = 1; idCounter <= Object.keys(percentageData).length; idCounter++) {
		    var currentSelected;
		    // if we call this function on initialization and no carriers are selected, all carriers get selected
		    // if there are some carriers preselected or this is not the first call, we don't change anything
		    if (init && carrierService.isEmpty()) {
			currentSelected = true;
		    }
		    else {
			currentSelected = carrierService.hasCarrier(idCounter);
		    }
		    $scope.carriers.push({id:idCounter, selected:currentSelected, color:percentageService.getColorOfCarrier(percentageData[idCounter])});
		}
		$scope.createFlexibilityChart();
	    });
    }

    $scope.reload = function() {
	sessionService.setCurrentSession($scope.currentSession);
	$scope.currentFileName = sessionService.getDataFileNameById($scope.currentSession);
	updateCarrierArrayAndDrawGraph(false);
    }

    // this function ic called, when the user enters the graph page for the first time.
    // It will draw the graph and sets the selected carriers to a default value.
    $scope.init = function() {
	updateCarrierArrayAndDrawGraph(true);
        // if (carrierService.isEmpty()) {
	//    carrierService.selectAll();
	// }
        $scope.reload;
    }

    $scope.$on("$destroy", function() {
	if(carrierService.containsAllUpTo($scope.carriers.length)) {
	    carrierService.emptyCarrierArray();
	}
    });
    
    /* this functions creates the dygraph from a data source and applies options to them*/
    $scope.createFlexibilityChart = function() {

        sessionService.setCurrentSession($scope.currentSession);

        // create the graph with the parameters set. The request path for the database depends on 3 parameters: carrierRequested, selectedIteration and selectedSession
        // the url which should be requested wil be defined in requestedUrl
        // to allow to export the csv file the variable is defined as a $scope variable
        $scope.requestedUrl = 'django/dataInterface/continuousDataAbsoluteTime.csv?carriers='+$scope.carriersRequested()+'&iterations='+$scope.selectedIteration+'&dimension=speed&session='+$scope.currentSession+'';

        // Download file
        $scope.downloadFile = function(){
            window.location = $scope.requestedUrl;
        }

        graph = new Dygraph(
	       document.getElementById("FlexibilityChart"),$scope.requestedUrl , {title: 'Flexibility Graph',
	                                                                          ylabel: 'Speed',
	                                                                          xlabel: 'Absolute Time in ms',
	                                                                          labelsSeparateLines: true,
	                                                                          highlightSeriesOpts: {
	                                                                            strokeWidth: 4,
	                                                                            strokeBorderWidth: 1,
	                                                                            highlightCircleSize: 5
	                                                                          },
	                                                                          legend: "always",
	                                                                          /*labelDiv looks for an element with the given id and puts the legend into this element.
	                                                                          Therefore the legend will not bis displayed inside the graph */
	                                                                          labelsDiv: document.getElementById("FlexibilityChartLegend"),
	                                                                          axes: {
                                                                                    x: {
                                                                                        /* formatting the x axis label in the legend. Now it will display not only the value but also a text */
                                                                                        valueFormatter: function(x) {
                                                                                            return 'Absolute time ' + x;
                                                                                        },
                                                                                        // Only draw whole number integers as labels
                                                                                        axisLabelFormatter: function(x) {
                                                                                            if (x % 1 == 0) {
                                                                                                return x;
                                                                                            } else {
                                                                                                return "";
                                                                                            }
                                                                                        }
                                                                                    }
                                                                              },
	                                                                          });

	$scope.getListStyle = function(index) {
            if (index % 5 == 1) {
                return {'clear': 'left'};
            }
            else {
                return {};
            }
        }

        // Update the flex measure for the new selection
        $scope.flexibilityMeasure = calculateFlexibilityMeasure();

        $scope.updateFileName = function() {
	        $scope.currentFileName = sessionService.getCurrentDataFileName($scope.currentSession);
	    }

        // Updates the  time for the time stamp
        $scope.ts = new Date();
    }
})

/* from here on, all controllers are for the scrolling to elements in a page */

.controller('ScrollController', function ($scope, $location, $anchorScroll) {

    /* anchor scrolls to the id, injected into the location hash.
       then activates scroll
    */
    $scope.scrollTo = function(id) {
        var old = $location.hash();
        $location.hash(id);
        $anchorScroll();
        $location.hash(old);
    };
})
