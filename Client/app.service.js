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



/* This file contains all AngularJS Services*/

angular.module('app')

.service('percentageService', function(sessionService, $timeout, $http) {
    /*
      Provides percentage data of carriers
    */
    var percentageDataPromise;
    var percentageData = [];
    var flag = false;
    function getFromDB(percentageDataType) {
        /*
          Fetches data from backend and sends it to the controller. This will only be done, once the parsing is completed
          So far this is called each time when getAll is called, but this is probably not necessary
        */
	percentageDataPromise = $http.get('django/dataInterface/percentages.json?session=' +sessionService.getCurrentSession() + '&type='+percentageDataType);
    }
    
    this.getAll = function(percentageDataType) {
        getFromDB(percentageDataType);
	percentageDataPromise.then(function(result) {percentageData = result.data});
        return percentageData;
    }
    
    this.getPercentagePromise = function(percentageDataType) {
	return $http.get('django/dataInterface/percentages.json?session=' +sessionService.getCurrentSession() + '&type='+percentageDataType);
    }

    this.getColorOfCarrier = function(carrier) {
        var percentageOfEnergy = percentageData[carrier];
        var color = {'background-color': 'rgb(255,255,0)'};
	
        if(percentageOfEnergy > 1.05) {
            color = {'background-color' : 'rgb(229, 28, 52)'};
        }

        if(percentageOfEnergy <= 1.025 ) {
            color = {'background-color' : 'rgb(178,255,89)'};
        }
        return color;
    }


    return {
        getAll: this.getAll,
        getColorOfCarrier: this.getColorOfCarrier,
	getPercentagePromise: this.getPercentagePromise,
    };
});

/* The carrierService, proved carrier data to all controllers
For now it is used to saves the carriers for comparison, chosen by the user and proved them to all controller
who need the data.
*/

angular.module('app')

.service('carrierService', function(sessionService) {
    var carriersForComparison = [];

    this.containsCarrier = function(carrierID){
        for(var i = 0; i < carriersForComparison.length; i++) {
            if (carriersForComparison[i].carrierNumber == carrierID) {
                return true;
            }
        }
        return false;
    }

    this.hasCarrier = function(carrierId) {
	    return carriersForComparison.some(function(carrier){return carrier.carrierNumber == carrierId;});
    }
    
    // function adds a carrier with a given ID
    this.addCarrier = function(newCarrier) {
        console.log("add Carrier");
        for(var i = 0; i < carriersForComparison.length; i++) {
            if (carriersForComparison[i].carrierNumber == newCarrier) {
                return false;
            }
        }
        carriersForComparison.push({carrierNumber: newCarrier});
        return true;
    };

    // returns the array with CarrierIDs to be compared
    this.getCarrier = function(){
        return carriersForComparison;
    }

    // deletes a carrier with a given ID
    this.deleteCarrier = function(removeCarrier) {
        for(var i = 0; i < carriersForComparison.length; i++) {
            if (carriersForComparison[i].carrierNumber == removeCarrier) {
                carriersForComparison.splice(i,1);
                return true;
            }
        }
        return false;
    }

    // this function empties the array, so that no carrier item is left inside anymore.
    this.emptyCarrierArray = function() {
        console.log("emptyCarrierArray");
        carriersForComparison.splice(0,carriersForComparison.length);
    }

    // this service returns these functions to the caller for use
    return {
        containsCarrier: this.containsCarrier,
        hasCarrier: this.hasCarrier,
        addCarrier: this.addCarrier,
        getCarrier: this.getCarrier,
        deleteCarrier: this.deleteCarrier,
        emptyCarrierArray: this.emptyCarrierArray
    };
});


angular.module('app')

.service('sessionService', function($http) {
    var numberOfSessions = 0;
    var currentSession = 1;
    var sessionDataPromise;

    function update () {
	// once sessions are added to database when they are load (instead of when simulation finishes)
	// use sessionData also to set numberOfSessions
	//$http.get("django/dataInterface/rawData.json?table=sessiondata")
	//    .then(function (response){sessionData = response.data;});
	
	var xmlHttp = new XMLHttpRequest();
	// so far session, carrier and iteration have to be set - they are disregarded however
	xmlHttp.open( "GET", 'django/dataInterface/values.request?session=1&carrier=1&iteration=1&value=currentSession', false );
	xmlHttp.send(null);
	//parses Http-ResponseText to a decimal int
	numberOfSessions = parseInt(xmlHttp.responseText,10);
    }
    
    this.getNumberOfSessions = function() {
	update();
	return numberOfSessions;
    }

    this.getCurrentSession = function() {
	return currentSession;
    }

    this.setCurrentSession = function(newSession) {
	currentSession = newSession;
    }
    
    this.getSessionData = function() {
	update();
	var sessionDataPromise = $http.get("django/dataInterface/rawData.json?table=sessiondata");
	//sessionDataPromise.then(function(response){console.log(JSON.stringify(response.data))});
	return sessionDataPromise;
    }

    // Returns the string of session with sessionId
    this.getDataFileNameById = function(id) {
	// Gets the full string of all data paths of all data files on the server
        var xmlHttp = new XMLHttpRequest();
        xmlHttp.open( "GET", 'django/dataInterface/simulation.files', false);
        xmlHttp.send(null);
        var string  = xmlHttp.responseText;

        // Separates the comma separated data files string to an array
        var arraySimulationFileNames = string.split(',');

        // Deletes the file path for every file name so that only the file name is displayed
        for (var i = 0; i < arraySimulationFileNames.length; i++) {
            arraySimulationFileNames[i] = arraySimulationFileNames[i].substring(32);
        }

        return arraySimulationFileNames[id - 1];
    }

    // Returns the string of the currently selected data file name
    this.getCurrentDataFileName = function() {
	return this.getDataFileNameById(currentSession);
    }
    
    return {
        getNumberOfSessions: this.getNumberOfSessions,
        getCurrentSession: this.getCurrentSession,
        setCurrentSession: this.setCurrentSession,
	getSessionData: this.getSessionData,
	getCurrentDataFileName: this.getCurrentDataFileName,
	getDataFileNameById: this.getDataFileNameById,
    };
	
});
