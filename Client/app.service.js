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

.service('percentageService', function(sessionService) {
    /*
    Provides percentage data of carriers
    */
    var percentageData = [];
    function getFromDB(percentageDataType) {
        /*
        Fetches data from backend
        So far this is called each time when getAll is called, but this is probably not necessary
        */
        Papa.parse('django/dataInterface/'+percentageDataType+'?session=' +sessionService.getCurrentSession(), {
            download: true,
            dynamicTyping: true,
            complete: function(results) {
                percentageData = results.data[1];
            }
        });
    }

    this.getAll = function(percentageDataType) {
        getFromDB(percentageDataType);
        return percentageData;
    }

    this.getColorOfCarrier = function(carrier) {
        var percentageOfEnergy = percentageData[carrier - 1];
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
        getColorOfCarrier: this.getColorOfCarrier
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

.service('sessionService', function() {
	var numberOfSessions = 0;
	var currentSession = 1;

	function update () {
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
	    update();
	    return currentSession;
	}

	this.setCurrentSession = function(newSession) {
		currentSession = newSession;
	}

	return {
        getNumberOfSessions: this.getNumberOfSessions,
        getCurrentSession: this.getCurrentSession,
        setCurrentSession: this.setCurrentSession,
	};
	
});
