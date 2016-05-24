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



/* This file contains all Angualr JS Services*/

angular.module('app')

/* The carrierService, proved carrier data to all controllers
For now it is used to saves the carriers for comparison, chosen by the user and proved them to all controller
who need the data.
*/

.service('carrierService', function() {
    var carriersForComparison = [];

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
         var toDelete =  carriersForComparison.indexOf(removeCarrier);
         carriersForComparison.splice(toDelete,1);
    }

    // this function empties the array, so that no carrier item is left inside anymore.
    this.emptyCarrierArray = function() {
        carriersForComparison.splice(0,carriersForComparison.length);
    }


     // this service returns 4 functions to the caller, which he can use.
    return {
        addCarrier: this.addCarrier,
        getCarrier: this.getCarrier,
        deleteCarrier: this.deleteCarrier,
        emptyCarrierArray: this.emptyCarrierArray,
    };
});



