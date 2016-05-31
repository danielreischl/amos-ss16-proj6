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
	    document.getElementById("graphdiv2"), "django/dataInterface/data.csv?carrier="+$scope.selectedCarrier+"&iteration="+$scope.selectedIteration+"&dimension="+$scope.selectedDimension+"&type=PoC", {});
    }
})

/* controller for the compareGraph. Should display the comparison chart with all the carriers the user wants to compare*/
.controller('compareCircleGraph', function($scope, carrierService) {

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

    // default value for the dimension and yAxislabel
    var selectedDimension = "energyConsumption";
    var yAxisLabel = yAxisLabels[selectedDimension];

    // default value for the selected Iterations
    var selectedIteration = "lastTen";

    // the session requested from the database. For now it is fixed.
    var session = 1;

    //a string, which tells the database how many carrier the user is requesting.
    var carriersRequested = "";

    // Get the maxAmount of Carriers from the database and save it in a variable called amountOfCarriers
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", 'django/dataInterface/values.request?session='+session+'&carrier=1&iteration=1&value=amountOfCarriers', false );
    xmlHttp.send(null);
    var amountOfCarriers = xmlHttp.responseText;

    // Get the last iteration database and save it
    var xmlHttp2 = new XMLHttpRequest();
    xmlHttp2.open( "GET", 'django/dataInterface/values.request?session='+session+'&carrier=1&iteration=1&value=lastIteration', false );
    xmlHttp2.send(null);
    var amountOfIterations = xmlHttp.responseText;

    //create an array depending on the amount of carriers. The items of the array will be used to initialize the checkboxes.
    var arrayCarrier = [];
    var idCounter = 1;
    while(arrayCarrier.length < amountOfCarriers) {
        arrayCarrier.push(idCounter);
        idCounter++;
    }

    //
    // Start of $scope
    //

    // Fill the drop down menus with the items of the array.
    // The number of checkboxes depend on the amount of carriers in the database
    $scope.arrayCarrier = arrayCarrier;

    // This function is called, when a change is made in the checkbox field.
    $scope.changeCarrierToCompare = function(event) {
        //if the carrier is already inside the comparison array, then it will be removed.
        if(!carrierService.addCarrier(event.target.id)) {
            carrierService.deleteCarrier(event.target.id);
            document.getElementById(event.target.id).checked = false;
        } else {
            document.getElementById(event.target.id).checked = true;
        }
    }

    $scope.dimensions = [
        {name : "Energy Consumption", id: 'energyConsumption'},
        {name : "Position", id: 'positionAbsolute'},
	    {name : "Speed", id: 'speed'},
	    {name : "Acceleration", id: 'acceleration'},
	    {name : "drive", id : 'drive'},
    ]

    $scope.iterationDimensions = [
        {name : "Last 10", id: 'lastTen'},
	{name : 'Last', id : 'last'},
        {name : "All", id: 'all'}
    ]

    // Creates the dygraph from a data source and applies options to them
    $scope.createCompareGraph = function() {

        //ensure that the variable is empty, before saving the new request path into it
        carriersRequested = "";
        iterationsRequested = "";
        /* these loops have the purpose to see what carriers the user wants to compare
        and change request String path for the database. It will also set all checkboxes to true, which are corresponding to the carriers
        in the compare array */

        if(carrierCompareList.length != 0) {
            for (var i = 0; i < carrierCompareList.length; i++) {
                for (var carrier = 1; carrier <= amountOfCarriers; carrier++) {
                    if (carrierCompareList[i].carrierNumber == carrier) {
                        if(carriersRequested === "") {
                            carriersRequested+=carrier;
                        } else {
                            carriersRequested+= ","+carrier+"";
                        }
                        break;
                    } else {
                    }
                }
            }
        } else {
            alert("You did not chose any Carriers to compare")
        }

        var iterationsRequested = getSelectedIterationsString();

        graph = new Dygraph(
	        document.getElementById("compareGraph"),'django/dataInterface/continuousData.csv?carriers='+carriersRequested + '&iterations=' + iterationsRequested + '&dimension=' + selectedDimension + '&session=1',
	            {title: yAxisLabels[selectedDimension],
	            ylabel: yAxisLabels[selectedDimension]+' in '+units[selectedDimension],
	            xlabel: 'time in ms',
	            labelsSeparateLines: true,
	            highlightSeriesOpts: {strokeWidth: 4, strokeBorderWidth: 1, highlightCircleSize: 5},
	            });

	// After the graph has been plotted, the compareCarrier Array will be emptied and the checkboxes reseted.
	// disable for now
        carrierService.emptyCarrierArray();
        uncheckAllCheckboxes();
    }

    $scope.changeDimension = function() {
	    selectedDimension = $scope.selectedDimension;
	}

	$scope.changeIteration = function() {
	    selectedIteration = $scope.selectedIteration;
	}

	// This function empties the carriers in the comparison on page leave.
    // If the user leaves the current html snippet/template then,
    // this function will notice that and trigger the function "emptyCarrierArray"
    $scope.$on("$destroy", function() {
        carrierService.emptyCarrierArray();
    });

    //
    // Start of funciton
    //

    function getSelectedIterationsString() {
        var selectedIterationsString = "";
        var iter = 1;

        if(amountOfIterations <= 0) {
            return selectedIterationsString;
        }


	if (selectedIteration === "last") {
	    selectedIterationsString += amountOfIterations;
	}
	else {
	    if(selectedIteration === "lastTen") {
		iter = amountOfIterations - 10;
		if(iter < 1) {
		    iter = 1;
		}
	    }
            while(iter <= amountOfIterations) {
		selectedIterationsString += iter;
		if(iter != amountOfIterations) {
                    selectedIterationsString += ",";
		}
		iter += 1;
            }
	}
	
        return selectedIterationsString;
    }

    function uncheckAllCheckboxes() {
        var checkboxElements = document.getElementsByTagName('input');
        for (var i = 0; i < checkboxElements.length; i++) {
            if(checkboxElements[i].type == 'checkbox') {
                 checkboxElements[i].checked = false;
            }
        }
    }



})


/* controller for the AverageEnergyConsumption Chart. This chart will display the data over iterations. The user can select
which kind of data he wants to see. The default value is average energy consumption.*/
.controller('AverageEnergyConsumptionChart', function($scope, carrierService) {

    // get the array with the carriers the user wants to see in the graph.
    var carrierCompareList = carrierService.getCarrier();

    // y-Axis labels for different dimensions
    var yAxisLabels = {'energyConsumptionAverage' : 'Average Energy Consumption',
		       'accelerationAverage' : 'Average Acceleration',
		       'speedAverage': 'Average Speed',
		       'energyConsumptionTotal': 'Total Energy Consumption' };

    var units = {'energyConsumptionAverage': 'W',
		 'accelerationAverage' : '?',
		 'speedAverage': '?',
		 'energyConsumptionTotal': 'W' };

    // default value for the dimension and yAxislabel
    var selectedDimension = "energyConsumptionAverage";
    var yAxisLabel = yAxisLabels[selectedDimension];

    // the session requested from the database. For now it is fixed.
    var session = 1;

    //a string, which tells the database how many carrier the user is requesting.
    var carriersRequested = "";

    // Get the maxAmount of Carriers from the database and save it in a variable called amountOfCarriers
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", 'django/dataInterface/values.request?session='+session+'&carrier=1&iteration=1&value=amountOfCarriers', false );
    xmlHttp.send(null);
    var amountOfCarriers = xmlHttp.responseText;

    //create an array depending on the amount of carriers. The items of the array will be used to initialize the checkboxes.
    var arrayCarrier = [];
    var idCounter = 1;
    while(arrayCarrier.length < amountOfCarriers ) {
        arrayCarrier.push(idCounter);
        idCounter++;
    }
    /* Filling the Dropdown menues with the items of the array. The number of checkboxes depend on the amount of carriers in the database*/
    $scope.arrayCarrier = arrayCarrier;

    // showCheckBoxes is at startup false, because the checkboxes should be hidden.
    $scope.showCheckBoxes = false;

    // When the user clicks on the Button, showCheckBoxes changes to true/false, depending on the previous state.
    $scope.toggle = function(){
        $scope.showCheckBoxes = !$scope.showCheckBoxes;
    }

    // This function is called, when a change is made in the checkbox field.
    $scope.changeCarrierToCompare = function(event) {
        //if the carrier is already inside the comparison array, then it will be removed.
        if(!carrierService.addCarrier(event.target.id)) {
            carrierService.deleteCarrier(event.target.id);
            document.getElementById(event.target.id).checked = false;
        } else {
            document.getElementById(event.target.id).checked = true;
        }
    }

    // create the dropdown menu for iterations. the id is corresponding to the key word used in the database to extract the dimension.
    $scope.iterations = [
        {name : "Last 10 Iterations", id : 'lastTen'},
    ]

    // create the dropdown menu for dimensions. the id is corresponding to the key word used in the database to extract the dimension.
    $scope.dimensions = [
        {name : "Average Energy Consumption", id : 'energyConsumptionAverage'},
        {name : "Average Acceleration", id : 'accelerationAverage'},
	    {name : "Average Speed", id: 'speedAverage'},
	    {name : "Total Energy Consumption", id: 'energyConsumptionTotal'}
    ]


     // This function receives the changes from the dropDown menu "dimensions" and changes the yAxis name of the graph and requests the needed data by changing the string name.
     $scope.changeDimension = function() {
	    selectedDimension = $scope.selectedDimension;
	 }

    /* this functions creates the dygraph  from a data source and applies options to them*/

    $scope.createAverageEnergyConsumptionChart = function() {

        //ensure that the variable is empty, before saving the new request path into it
        carriersRequested = "";
        /* these loops have the purpose to see what carriers the user wants to compare
        and change request String path for the database. It will also set all checkboxes to true, which are corresponding to the carriers
        in the compare array */

        if(carrierCompareList.length != 0) {
            for (var i = 0; i < carrierCompareList.length; i++) {
                for (var carrier = 1; carrier <= amountOfCarriers; carrier++) {
                    if (carrierCompareList[i].carrierNumber == carrier) {
                        if(carriersRequested === "") {
                            carriersRequested+=carrier;
                        } else {
                            carriersRequested+= ","+carrier+"";
                        }
                        break;
                    } else {
                    }
                }
            }
        } else {
            alert("You did not chose any Carriers to compare")
        }

        // create the graph with the parameters set. The request path for the database depends on 3 parameters: session, carrierRequested and selectedDimension

        graph = new Dygraph(
	       document.getElementById("AverageEnergyConsumptionChart"), 'django/dataInterface/averageEnergyConsumption.csv?session='+session+'&carriers='+carriersRequested+'&dimension='+selectedDimension+'',
	                                                                                     {title: yAxisLabels[selectedDimension],
	                                                                                      ylabel: yAxisLabels[selectedDimension]+' in '+units[selectedDimension],
	                                                                                      xlabel: 'Iteration',
	                                                                                      labelsSeparateLines: true,
	                                                                                      highlightSeriesOpts: {strokeWidth: 4, strokeBorderWidth: 1, highlightCircleSize: 5},
	                                                                                      });


        // After the graph has been plotted, the compareCarrier Array will be emptied and the checkboxes reseted.
        carrierService.emptyCarrierArray();
        uncheckAllCheckboxes();
    }


    function uncheckAllCheckboxes() {
        var checkboxElements = document.getElementsByTagName('input');
        for (var i = 0; i < checkboxElements.length; i++) {
            if(checkboxElements[i].type == 'checkbox') {
                 checkboxElements[i].checked = false;
            }
        }
    }

     /* This function empties the carriers in the comparison on page leave.
     If the user leaves the current html snippet/template then, this function will notice that and trigger the function "emptyyCarrierArray" */
     $scope.$on("$destroy", function(){
         carrierService.emptyCarrierArray();
     });

})
   

/* Refresh the circle Page. The purpose of this controller is listen to the Button
 and upon receiving an event, it should trigger the update circle button*/
.controller('circleGraphController', function($scope, $compile, $mdDialog, $mdMedia, $timeout, $mdSidenav, carrierService) {


/* This function will highlight the carrier and save the id of the carrier inside the comaprison arrary in app.service.js*/
    $scope.selectCarrier = function(event) {
        // id = carrier x
        var id = event.target.id;
        // This method is necessary, because the string is "carrier x" To extract x, I need to get the subsstring
        var carrierId = id.substr(7, 8);

        //var circle = document.getElementById("carrier " + carrierId);
        var canvas = document.getElementById(id);
        var context = canvas.getContext('2d');
        var centerX = canvas.width / 2;
        var centerY = canvas.height / 2;
        var radius = 70;

        //check if carrier is already in list.
        if(!carrierService.addCarrier(carrierId)) {
            //Already in the list, remove the highlight
            context.beginPath();
            context.arc(centerX, centerY, radius, 0, 2 * Math.PI);
            context.lineWidth = 9;
            context.strokeStyle = "#ECEFF1";
            context.stroke();

            //If it exists delete the carrier
            carrierService.deleteCarrier(carrierId);
        } else {
            //Not in the list, highlight
            context.beginPath();
            context.arc(centerX, centerY, radius, 0, 2 * Math.PI);
            context.lineWidth = 7;
            context.strokeStyle = "#003300";
            context.stroke();
        }
    }

/* create the circle page upon page load. */
    $scope.circleGraph = function() {
    /* open connection to the REST API from the middleware and get the amount of carriers.
       After receiving the data, the integer variable will be saved inside of amountOfCarriers
    */
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", 'django/dataInterface/values.request?session=1&carrier=1&iteration=1&value=amountOfCarriers', false );
    xmlHttp.send(null);
    var amountOfCarriers = xmlHttp.responseText;
    /* ID of first Carrier */
    var idCounter = 1;
    // the array variable where the converted content from the csv file will be.
    var carrierPercentageData;
    // get the csv files with the percentages from the middleware, extract the exact array and save it into a variable.
    Papa.parse('django/dataInterface/percentages.csv?session=1', { download: true,
                                                                   dynamicTyping: true,
                                                                   complete: function(results) {
                                                                       carrierPercentageData =results.data[1];
                                                                   }
                                                                  }
    )

    //delay the creation of the circles by 1 second, so that the percentage data can be loaded into the function.
    $timeout(createCarrierHTML, 1000);

    // function to create HTML circle fragments dynamically
    function createCarrierHTML() {

        /* for every carrier in the database, create a new code fragment to be injected into the html file. Each fragment is the base for a circle */
        while (amountOfCarriers > 0) {
        var circleId = "carrier " + idCounter;
        var fragmenthtml = '<canvas class="circleDashboard" id="'+circleId+'" ng-click="selectCarrier($event)"></canvas>';
        var temp = $compile(fragmenthtml)($scope);

        // get the element in the html page, on which the new fragment should be appended to
        angular.element(document.getElementById('circleGraphs')).append(temp);

        // call the circle drawing method to paint the circles. It will get the ID of the carrier, as well as the percentage data
        createCircle(circleId, carrierPercentageData[idCounter - 1]);

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
        var percentageOfEnergyRounded = percentageOfEnergy.toFixed(2);

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
            context.fillStyle = '#FF1744';
        } else if(percentageOfEnergy <= 1.025 ) {
            context.fillStyle = '#00BFA5';
        } else {
            context.fillStyle = "#FFFF8D";
        }

        context.fill();
        context.lineWidth = 5;
        context.lineWidth = 1;
        context.fillStyle = "#212121";
        context.lineStyle = "#212121";
        context.font = "15px sans-serif";
        context.fillText(carrier, centerX - 15, centerY);
        context.fillText(percentageOfEnergyRounded*100 + "%", centerX - 15, centerY + 20);
    }
}

})


/*.controller('barchartController',function () {


    function barChartPlotter(e) {
  var ctx = e.drawingContext;
  var points = e.points;
  var y_bottom = e.dygraph.toDomYCoord(0);  // see <a href="http://dygraphs.com/jsdoc/symbols/Dygraph.html#toDomYCoord">jsdoc</a>

  // This should really be based on the minimum gap
  var bar_width = 2/3 * (points[1].canvasx - points[0].canvasx);
  ctx.fillStyle = e.color;  // a lighter shade might be more aesthetically pleasing

  // Do the actual plotting.
  for (var i = 0; i < points.length; i++) {
    var p = points[i];
    var center_x = p.canvasx;  // center of the bar

    ctx.fillRect(center_x - bar_width / 2, p.canvasy, bar_width, y_bottom - p.canvasy);
    ctx.strokeRect(center_x - bar_width / 2, p.canvasy, bar_width, y_bottom - p.canvasy);
  }
}
 var data = "Carrier,Percentage%\n" +
     "1,50\n" +
     "2,70\n" +
     "3,90\n" +
     "4,100\n" +
         "5,180\n" +
    "6,200\n" +
    "7,250\n" +
     "8,150\n";
g = new Dygraph(document.getElementById("graph"),data,


                 {
                         drawlineCallback: function (g, seriesName, ctx, cx, cy, seriesColor, pointSize, row) {
                             var col = g.indexFromSetName(seriesName);
                             var val = g.getValue(row, col);
                             var color = '';
                             if (val >= 0 && val <= 50) {
                                 color = 'green';
                             } else if (val > 50 && val <= 80) {
                                 color = 'yellow';
                             } else if (val > 80) {
                                 color = 'red';
                             }
                             if (color) {
                                
                        ctx.fillStyle = color;
                            
                             }
                         },

                     // options go here. See http://dygraphs.com/options.html
                     legend: 'always',
                     animatedZooms: true,
                     plotter: barChartPlotter,
                     






                     
                     axes: {
                            x: {
                                valueFormatter: function(x) {
                                    var ret;
                                    switch (x){
                                        case 1:
                                           ret = 'carrier1';                
                                           break;
                                        case 2:
                                           ret = 'carrier2';                
                                           break;
                                        case 3:
                                           ret = 'carrier3';                
                                           break;
                                        case 4:
                                           ret = 'carrier4';                
                                           break;
                                        case 5:
                                           ret = 'carrier5';                
                                           break;
                                        case 6:
                                           ret = 'carrier6';                
                                           break;
                                        case 7:
                                           ret = 'carrier7';                
                                           break;
                                        case 8:
                                           ret = 'carrier8';                
                                           break;                                            
                                    }
                                    return ret;
                                },
                                axisLabelFormatter: function(x) {
                                    var ret;
                                    switch (x){
                                        case 1:
                                           ret = 'carrier1';                
                                           break;
                                        case 2:
                                           ret = 'carrier2';                
                                           break;
                                        case 3:
                                           ret = 'carrier3';                
                                           break;
                                        case 4:
                                           ret = 'carrier4';                
                                           break;
                                        case 5:
                                           ret = 'carrier5';                
                                           break;
                                        case 6:
                                           ret = 'carrier6';                
                                           break;
                                        case 7:
                                           ret = 'carrier7';                
                                           break;
                                        case 8:
                                           ret = 'carrier8';                
                                           break;                                            
                                    }
                                    return ret;
                                }         
                            }                
                    },
                 });
                 



})

*/
/*.controller('chartMaker',function($scope) {

        $scope.chartParams = {
            listOfCarriers: ['carrier1', 'carrier2', 'carrier3', 'carrier4', 'carrier5', 'carrier6', 'carrier7', 'carrier8', 'carrier9', 'carrier10', 'carrier11', 'carrier12', 'carrier13', 'carrier14', 'carrier15'],
            dataset: [[80, 100, 60, 90, 150, 200, 100, 170, 100, 75, 120, 250, 170, 300, 280]],
            series: ["energy consumption"],
            label: 'percentage',
            colours: [{fillColor: ["#FF0000", "#00FF00", "#FF0000", "##FFFF00", "#FFFF00", "#FF0000", "#FF0000", "#00FF00", "#FFFF00", "#00FF00", "#FF0000", "#FF0000", "#FF0000", "#FF0000", "#FF0000"]}],
          
            options: {barShowStroke: false},
            options: {
                // String - Template string for single tooltips
                tooltipTemplate: "<%if (label){%><%=label %>: <%}%><%= value + '%' %>",


                scaleLabel: "<%= value + '%' %>",
            },

            /* ctx : document.getElementById("locationBar").getContext("2d")



            }

        }



)*/
    
.controller('chartMaker',function($scope) {

    var barChartData = {
    labels: ["carrier1", "carrier2", "carrier3","carrier4","carrier5","carrier6","carrier7","carrier8"],
    datasets: [
        {
            yAxisLabel: "My Y Axis Label",
            fillColor: "rgba(220,220,220,0.5)", 
            strokeColor: "rgba(220,220,220,0.8)", 
            highlightFill: "rgba(220,220,220,0.75)",
            highlightStroke: "rgba(220,220,220,1)",
            data: [100, 150, 200, 75, 250, 80, 130, 60]
            
          
        }
    ],
        

};


    var ctx = document.getElementById("mycanvas").getContext("2d");
    window.myObjBar = new Chart(ctx).Bar(barChartData, {
          responsive : true,
        scaleLabel: "<%= value %> %",


        showTooltips: false,
    onAnimationComplete: function () {

        var ctx = this.chart.ctx;
        ctx.font = this.scale.font;
        ctx.fillStyle = this.scale.textColor
        ctx.textAlign = "center";
        ctx.textBaseline = "bottom";

        this.datasets.forEach(function (dataset) {
            dataset.bars.forEach(function (bar) {
                ctx.fillText(bar.value, bar.x, bar.y - 5);
            });
        })
    }

    });

     var bars = myObjBar.datasets[0].bars;
    for(i=0;i<bars.length;i++){
       var color="green";
       
       if(bars[i].value<=100){
       	color="yellow";
       }
       else if(bars[i].value<=150){
       	color="green"
          
       
       }
       else if(bars[i].value<=200){
       	color="red"
       }
       else{
       	color="red"
       }
       
       bars[i].fillColor = color;
        bars[i].highlightFill = color;

    }
    myObjBar.update(); //update the cahrt


}
)




