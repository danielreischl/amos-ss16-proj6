/* This file contains all Angualr JS Services*/

angular.module('app')

/* The carrierService, proved carrier data to all controllers
For now it is used to saves the carriers for comparison, chosen by the user and proved them to all controller
who need the data.
*/

.service('carrierService', function() {
    var carriersForComparison = [];

    this.addCarrier = function(newCarrier) {
         carriersForComparison.push({carrierNumber: newCarrier});
    };

    this.getCarrier = function(){
        return carriersForComparison;
    }

    this.deleteCarrier = function(removeCarrier) {
         var toDelete =  carriersForComparison.indexOf(removeCarrier);
         carriersForComparison.splice(toDelete,1);
    }

    return {
        addCarrier: this.addCarrier,
        getCarrier: this.getCarrier,
        deleteCarrier: this.deleteCarrier,
    };
});



