import csv
from django.shortcuts import render
from django.http import HttpResponse
from helloWorld.models import timestampdata
from django.db.models import Max

# Funtion to return values instead of csv - Files
def db2values (request):

    # possible paramaters:
    # session, carrier, value (Which value should be returned)
    requestedSession = request.GET['session']
    requestedCarrier = request.GET['carrier']
    requestedValue = request.GET['value']

    # If requested Value is LastItteration of a carrier:
    if requestedValue=='LastItteration':
        # Returns the LastIterration of the called Carrier and Session, returns the max Value in the db (Iterations are counted in the db)
        return HttpResponse(timestampdata.objects.filter(session=requestedSession,carrier=requestedCarrier).aggregate(Max('iteration')))
    # Returns 15 as AmountOfCarriers
    # TODO: Read it out from setConstants.py
    if requestedValue=='AmountOfCarriers':
        return HttpResponse('15')



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


    result = timestampdata.objects.filter(carrier=requestedCarrier,iteration=requestedIteration)


    writer = csv.writer(response)

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


def index(request):
    context = {'toGreet': 'World'}
    return render(request, 'helloWorld/index.html', context)

