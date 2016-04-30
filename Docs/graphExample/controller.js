'use strict';
// definieren eines Moduls
var app = angular.module('visuModule', []);

// hinzufügen eines Controllers zum Modul

app.controller('visuController', function($scope) {
    $scope.graphs = [
        {name : "Acceleration", file : "dummy.csv"},
        {name : "Power", file : "dummy2.csv"},
	];
    $scope.paintGraph = function(file) {
	g2 = new Dygraph(
	    document.getElementById("graphdiv2"), file, {});
    }
});
