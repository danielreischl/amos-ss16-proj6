#   This file is part of Rogue Vision.
#
#   Copyright (C) 2016 Daniel Reischl, Rene Rathmann, Peter Tan,
#       Tobias Dorsch, Shefali Shukla, Vignesh Govindarajulu,
#       Aleksander Penew, Abinav Puri
#
#   ReqTracker is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   ReqTracker is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PUROSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with rogueVision.  If not, see <http://www.gnu.org/licenses/>.

import csv
from django.shortcuts import render
from django.http import HttpResponse
from dataInterface.models import timestampdata
from dataInterface.models import iterationdata
from django.db.models import Max

# Funtion to return values instead of csv - Files
def db2values (request):

    # possible paramaters:
    # session, carrier, value (Which value should be returned)
    requestedSession = request.GET['session']
    requestedCarrier = request.GET['carrier']
    requestedIteration = request.GET['iteration']
    requestedValue = request.GET['value']

    # If requested Value is LastItteration of a carrier:
    if requestedValue=='lastIteration':
        # Returns the LastIterration of the called Carrier and Session, returns the max Value in the db (Iterations are counted in the db)
        return HttpResponse(timestampdata.objects.filter(session=requestedSession,carrier=requestedCarrier).aggregate(Max('iteration')))
    # Returns 15 as AmountOfCarriers
    # TODO: Read amountOfCarriers and Session out from setConstants.py
    elif requestedValue=='amountOfCarriers':
        return HttpResponse('8')
    # returns current session
    elif requestedValue=='currentSession':
        return HttpResponse('1')
    # returns Average Energy Consumption of a specific carrier in a specific iteration and session
    elif requestedValue=='energyConsumptionAverage':
        return HttpResponse(iterationdata.objects.get(session=requestedSession,carrier=requestedCarrier,iteration=requestedIteration).energyConsumptionAverage)
    # returns Average Speed of a specific carrier in a specific iteration and session
    elif requestedValue == 'speedAverage':
        return HttpResponse(iterationdata.objects.get(session=requestedSession,carrier=requestedCarrier,iteration=requestedIteration).speedAverage)
    # returns Total Energy Consumption of a specific carrier in a specific iteration and session
    elif requestedValue == 'energyConsumptionTotal':
        return HttpResponse(iterationdata.objects.get(session=requestedSession,carrier=requestedCarrier,iteration=requestedIteration).energyConsumptionTotal)
    # return Average Acceleration of a specific carrier in a specific iteration and session
    elif requestedValue == 'accelerationAverage':
        return HttpResponse(iterationdata.objects.get(session=requestedSession,carrier=requestedCarrier,iteration=requestedIteration).accelerationAverage)


def db2csv(request):
    # returns a csv File according to the parameters given in the URL
    # possible parameters: carrier, timeSpan, iterations etc
    # exact functionality to be specified, at the moment this is just a proof of concept
    response = HttpResponse(content_type='text/csv')
    # the name data.csv is just used by the browser when you query the file directly and want to download it
    response['Content-Disposition'] = 'attachment; filename="data.csv"'

    # extract parameters
    # e.g. for first carrier request position.csv?carrier=1
    requestedCarrier = request.GET['carrier']
    requestedIteration = request.GET['iteration']
    requestedDimension = request.GET['dimension']
    requestedExtractionType = request.GET['type']

    writer = csv.writer(response)

    if requestedExtractionType == "PoC":
        result = timestampdata.objects.filter(carrier=requestedCarrier,iteration=requestedIteration)

        # case analysis by the selected dimension: there must be a nicer way to do this
    
        if requestedDimension == "POSITION":
            for row in result:
                writer.writerow([row.timeStamp, row.positionAbsolute])
        elif requestedDimension == "ACCELERATION":
            for row in result:
                writer.writerow([row.timeStamp, row.acceleration])
        elif requestedDimension == "SPEED":
            for row in result:
                writer.writerow([row.timeStamp, row.speed])
        elif requestedDimension == "ENERGY":
            for row in result:
                writer.writerow([row.timeStamp, row.energyConsumption])
            
    return response

def rawData(request):
    # returns a csv File of the raw database tables 
    # parameter table, possible values: timestampdata, iterationdata 
    response = HttpResponse(content_type='text/csv')
    # the name data.csv is just used by the browser when you query the file directly and want to download it
    response['Content-Disposition'] = 'attachment; filename="rawData.csv"'
    writer = csv.writer(response)
    
    # extract parameters
    requestedTable = request.GET['table']

    if requestedTable == "TIMESTAMP":
        result = timestampdata.objects.all()
        for row in result:
            # todo: get all columns
            writer.writerow([row.timeStamp, row.positionAbsolute])

    elif requestedTable == "ITERATION":
        result = iterationdata.objects.all()
        for row in result:
            # todo: get all columns
            writer.writerow([row.session, row.carrier, row.speedAverage])
            
    return response

def logs(request):

    # Returns a Textfile
    # parameter type, possiblie Values: DataProcessing
    requestedType = request.GET['type']
    response['Content-Disposition'] = 'attachment; filename="Log.text"'

    if requestedType == "DataProcessing":
        response = HttpResponse("srv/DataProcessing/DataProcessing.log",content_type='text/csv' )
        return response

def index(request):
    context = {'toGreet': 'World'}
    return render(request, 'dataInterface/index.html', context)

