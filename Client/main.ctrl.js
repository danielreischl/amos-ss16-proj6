/*
   This file is part of Roguevison.

   Copyright (C) 2016 Daniel Reischl, Rene Rathmann, Peter Tan,
       Tobias Dorsch, Shefali Shukla, Vignesh Govindarajulu,
       Aleksander Penew, Abinav Puri

   ReqTracker is free software: you can redistribute it and/or modify
   it under the terms of the GNU Affero General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   ReqTracker is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PUROSE.  See the
   GNU Affero General Public License for more details.

   You should have received a copy of the GNU Affero General Public License
   along with ReqTracker.  If not, see <http://www.gnu.org/licenses/>.
*/



/* This file should list all main controllers */

angular.module('app')

.controller("MainController", function(){
    var vm = this;
    vm.title = 'Siemens Data Analytics App';
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
    var visibilityArray = [false, false, false, false, false, false, false, false, false, false]; //this needs to be dynamic later if we have connection to the database! 1ßx booleans because of 2 extra comas in the csv.
    var arrayCarrier = [0,1,2,3,4,5,6,7];


    $scope.arrayCarrier = arrayCarrier;

    //changes the visibility from true to false and vice versa, depending on the checkboxes.

    $scope.change = function(event) {

        if(visibilityArray[event.target.id]) {
            visibilityArray[event.target.id] = false;
        } else {
            visibilityArray[event.target.id] = true;
        }
    }




    /* this functions created the dygraph  from a data source and applies options to them*/

    $scope.createCompareGraph = function() {
        graph = new Dygraph(
	       document.getElementById("compareGraph"), 'sections/compareCarrier/dummy.csv', {title: "Carrier's energy consumption of the latest iteration",
	                                                                                      ylabel: 'Energy Consumption in (mA)',
	                                                                                      xlabel: 'Time in (ms)',
	                                                                                      labelsSeparateLines: true,
	                                                                                      highlightSeriesOpts: {strokeWidth: 4, strokeBorderWidth: 1, highlightCircleSize: 5},
	                                                                                      visibility: visibilityArray,
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


/* controller for the drillDown graph. This will show only the carrier selected by drilling Down. Furtheremore it will enable the user to
add more lines and get different details.*/

.controller('drillDownGraph', function($scope, carrierService) {

    var carrierCompareList = carrierService.getCarrier();
    var carrierMax = 8; //this needs to be dynamic later if we have connection to the database
    var visibilityArray = [false, false, false, false, false, false, false, false, false, false]; //this needs to be dynamic later if we have connection to the database! 1ßx booleans because of 2 extra comas in the csv.
    var arrayCarrier = [0,1,2,3,4,5,6,7];

 /* Filling the Dropdown menues with options*/
    $scope.arrayCarrier = arrayCarrier;

    $scope.dimensions = [
        {name : "Average Energy Consumption", id : "ENERGY"},
        {name : "Average Acceleration", id : "ACCELERATION"},
	    {name : "Average Speed", id: "SPEED"},
	    ]


/*chooses one carrier depending on the chosen option. this is done by emptying the comparison Array,
 changing the visibillity array and adding a single carrier to the comparison array in the end.. */


    $scope.changeVisibility = function() {
        carrierService.emptyCarrierArray();
        for(var i = 0; i < visibilityArray.length; i++) {
            visibilityArray[i] = false;
        }
        carrierService.addCarrier($scope.selectedCarrier);
    }
    /* this functions created the dygraph  from a data source and applies options to them*/

    $scope.createDrillDownGraph = function() {
        graph = new Dygraph(
	       document.getElementById("drillDownGraph"), 'sections/drillDownChart/dummy3.csv', {title: "Carrier Drilldown ",
	                                                                                      ylabel: 'Energy Consumption in (mA)',
	                                                                                      xlabel: 'Iteration',
	                                                                                      plotter: barChartPlotter,
	                                                                                      labelsSeparateLines: true,
	                                                                                      highlightSeriesOpts: {strokeWidth: 4, strokeBorderWidth: 1, highlightCircleSize: 5},
	                                                                                      visibility: visibilityArray,
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

    // this functions changes the plotting of the dygraph to bars instead of lines. /7 need to understand and change it

    function barChartPlotter(e) {
        var ctx = e.drawingContext;
        var points = e.points;
        var y_bottom = e.dygraph.toDomYCoord(0);
        var bar_width = 2/3 * (points[1].canvasx - points[0].canvasx);
        ctx.fillStyle = e.color;

        for (var i = 0; i < points.length; i++) {
            var p = points[i];
            var center_x = p.canvasx;
            ctx.fillRect(center_x - bar_width / 2, p.canvasy,
            bar_width, y_bottom - p.canvasy);
            ctx.strokeRect(center_x - bar_width / 2, p.canvasy,
            bar_width, y_bottom - p.canvasy);
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

    //This function will empty first all carriers left in the comparison sidenav AND only add the carrier selected to it. Then it will jump to the comparison chart directly..
    $scope.drillDown = function() {
        carrierService.emptyCarrierArray;
        carrierService.addCarrier(carrierId);
        $mdDialog.hide();
        window.location.href ="#drillDownChart";
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

    /* for each carrier in the array, create a new code fragment to be injected into the hdtml file. Each fragment is the base for a circle */

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

        /* depending on the ratio energy to average Energy, the color changes */

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
.controller('chartMaker',function($scope) {

        $scope.chartParams = {
            listOfCarriers: ['carrier1', 'carrier2', 'carrier3', 'carrier4', 'carrier5', 'carrier6', 'carrier7', 'carrier8','carrier9','carrier10','carrier11','carrier12','carrier13','carrier14','carrier15'],
            percentage: [[80, 100, 60, 90, 150, 200, 100, 170, 100, 75, 120, 250, 170,300, 280]],
            series: ["energy consumption"],
            label:'percentage',
            colours: [{fillColor: ["#FF0000", "#00FF00", "#FF0000", "##FFFF00", "#FFFF00", "#FF0000", "#FF0000", "#00FF00", "#FFFF00", "#00FF00", "#FF0000", "#FF0000", "#FF0000", "#FF0000", "#FF0000"]}],

            options: {barShowStroke: false},
            options : {
    // String - Template string for single tooltips
    tooltipTemplate: "<%if (label){%><%=label %>: <%}%><%= value + '%' %>",
    

    scaleLabel : "<%= value + '%' %>",
},
            /* ctx : document.getElementById("locationBar").getContext("2d")*/

            options: {
                customTooltips: function (tooltip) {
                    var tooltipEl = $('#chartjs-tooltip');

                    if (!tooltip) {
                        tooltipEl.css({
                            opacity: 0
                        });
                        return;
                    }

                    tooltipEl.removeClass('above below');
                    tooltipEl.addClass(tooltip.yAlign);

                    // split out the label and value and make your own tooltip here
                    var parts = tooltip.text.split(":");
                   var innerHtml = '<img src="assets/images/ic_add_circle_black_24px.svg"> <p> Add to comparison pane</p> <img src="assets/images/ic_zoom_in_black_24px.svg"><p>Drill down</p> <span>' + parts[0].trim() + '</span> : <span><b>' + parts[1].trim() + '</b></span>';
                    tooltipEl.html(innerHtml);

                    tooltipEl.css({
                        opacity: 1,
                        left: tooltip.chart.canvas.offsetLeft + tooltip.x + 'px',
                        top: tooltip.chart.canvas.offsetTop + tooltip.y + 'px',
                        fontFamily: tooltip.fontFamily,
                        fontSize: tooltip.fontSize,
                        fontStyle: tooltip.fontStyle,
                    });
                }

            }

    }
        }
    
)
    






