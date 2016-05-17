import csv
from django.shortcuts import render
from django.http import HttpResponse
from helloWorld.models import timestampdata


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

