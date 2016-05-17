import csv
from django.shortcuts import render
from django.http import HttpResponse


def db2csv(request):
    # returns a csv File according to the parameters given in the URL
    # possible parameters: carrier, timeSpan, iterations etc
    # exact functionality to be specified, at the moment this is just a proof of concept

    response = HttpResponse(content_type='text/csv')
    # the name data.csv is just used by the browser when you query the file directly and want to download it
    response['Content-Disposition'] = 'attachment; filename="data.csv"'

    # extract parameters
    # e.g. for first carrier request position.csv?carrier=1
    carrier = request.GET['carrier']
    

    # very simplistic test data
    # later this data is fetched from the DB according to parameters
    
    csv_test_data = (
        ('1', '0', '0', '5'),
        ('1', '1', '50', '5'),
        ('1', '2', '100', '5'),
        ('1', '3', '200', '5'),
        ('1', '4', '250', '5'),
        ('2', '3', '0', '5'),
        ('2', '4', '50', '10'),
        ('2', '5', '100', '10'),
        ('2', '6', '200', '5'),
        ('2', '7', '200', '5'),
    )
    
    writer = csv.writer(response)
    for row in csv_test_data:
        if (row[0] == carrier):
            writer.writerow([row[1],row[3]])


    return response


def index(request):
    context = {'toGreet': 'World'}
    return render(request, 'helloWorld/index.html', context)

