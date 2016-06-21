#   This file is part of Rogue Vision.
#
#   Copyright (C) 2016 Daniel Reischl, Rene Rathmann, Peter Tan,
#       Tobias Dorsch, Shefali Shukla, Vignesh Govindarajulu,
#       Aleksander Penew, Abhinav Puri
#
#   Rogue Vision is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   Rogue Vision is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with Rogue Vision.  If not, see <http://www.gnu.org/licenses/>.

import csv
from django.http import HttpResponse
from dataInterface.models import timestampdata
from dataInterface.models import iterationdata
from dataInterface.models import sessiondata
from django.db.models import Max
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
import sys

# Adds DataProcessing Path to Sys
sys.path.append('/srv/DataProcessing')
# imports dataProcessingFunctions
import dataProcessingFunctions
# imports subprocess to call shell
import subprocess


# Returns last iteration of a carrier at a session
def funcMaxIteration(session, carrier):
    return timestampdata.objects.filter(session=session, carrier=carrier).aggregate(Max('iteration')).get(
        'iteration__max')


# Returns total energy consumption of a carrier in a paticular session and iteration
def funcTotalEnergyConsumption(session, carrier, iteration):
    return iterationdata.objects.get(session=session, carrier=carrier, iteration=iteration).energyConsumptionTotal


# Returns average Speed of a carrier in a paticular session and iteration
def funcSpeedAverage(session, carrier, iteration):
    return iterationdata.objects.get(session=session, carrier=carrier, iteration=iteration).speedAverage


# Returns average energy consumption of a carrier in a paticular session and iteration
def funcAverageEnergyConsumption(session, carrier, iteration):
    return iterationdata.objects.get(session=session, carrier=carrier, iteration=iteration).energyConsumptionAverage


# Returns average acceleration of a carrier in a paticular session and iteration
def funcAccelerationAverage(session, carrier, iteration):
    return iterationdata.objects.get(session=session, carrier=carrier, iteration=iteration).accelerationAverage


# Returns the amount of carriers in a specific session
def funcAmountOfCarriers(session):
    return timestampdata.objects.filter(session=session).aggregate(Max('carrier')).get('carrier__max')


# Returns the most recent session
def funcRecentSession():
    return timestampdata.objects.all().aggregate(Max('session')).get('session__max')


# Returns one percent value for CarrierView & BarchartView calculated for creeping Contamination
def funcPercentCreeping(session, carrier):
    # TODO: Change to new Calculation
    # If there are less then 10 iterations
    if funcMaxIteration(session, carrier) < 10:
        # Consumption at first iteration
        initialConsumption = funcTotalEnergyConsumption(session, carrier, 1)
        # Consumption at current iteration
        lastConsumption = funcTotalEnergyConsumption(session, carrier, funcMaxIteration(session, carrier))
        # Divides last Consumption by First Consumption and retunrs it
        return lastConsumption / initialConsumption
    # If more then 10 iterations
    else:
        # Calculate first 10 percent of Iterations and Cast it to an int
        countOfIterations = int(funcMaxIteration(session, carrier) / 10)
        sumOfEnergy = 0
        # Sums up all energy consumptions
        for i in range(1, countOfIterations):
            sumOfEnergy = sumOfEnergy + funcTotalEnergyConsumption(session, carrier, i)
        # Consumption of current iteration
        lastConsumption = funcTotalEnergyConsumption(session, carrier, funcMaxIteration(session, carrier))
        # Calculates average consumption of first 10% of iterations
        initialConsumption = sumOfEnergy / countOfIterations
        # Divides current consumption by the average of the first 10 percents
        return (lastConsumption / initialConsumption)


# Returns one percent value for CarrierView & BarchartView calculated for continuous Contamination
def funcPercentCont(requestedSession, carrier):
    # TODO: Implement Calculation
    return 0


# Returns one percent value for CarrierView & BarchartView
def funcPecentageOfConsumption(session, carrier):
    # Consumption at first iteration
    initialConsumption = funcTotalEnergyConsumption(session, carrier, 1)
    # Consumption at current iteration
    lastConsumption = funcTotalEnergyConsumption(session, carrier, funcMaxIteration(session, carrier))
    # Divides last Consumption by First Consumption and returns it
    return (lastConsumption / initialConsumption)


###############################################
############ URL: values.request ##############
###############################################

# Function to return values instead of csv - Files
def db2values(request):
    # possible parameters:
    # session, carrier, value (Which value should be returned)
    requestedSession = request.GET['session']
    requestedCarrier = request.GET['carrier']
    requestedIteration = request.GET['iteration']
    requestedValue = request.GET['value']

    # If requested Value is LastIteration of a carrier:
    # Returns the LastIteration of the called Carrier and Session, returns the max Value in the db
    # (Iterations are counted in the db)
    if requestedValue == 'lastIteration':
        return HttpResponse(funcMaxIteration(requestedSession, requestedCarrier))
    # Returns AmountOfCarriers of a specific session
    elif requestedValue == 'amountOfCarriers':
        return HttpResponse(funcAmountOfCarriers(requestedSession))
    # returns current session
    elif requestedValue == 'currentSession':
        return HttpResponse(funcRecentSession())
    # returns Average Energy Consumption of a specific carrier in a specific iteration and session
    elif requestedValue == 'energyConsumptionAverage':
        return HttpResponse(funcSpeedAverage(requestedSession, requestedCarrier, requestedIteration))
    # returns Average Speed of a specific carrier in a specific iteration and session
    elif requestedValue == 'speedAverage':
        return HttpResponse(funcSpeedAverage(requestedSession, requestedCarrier, requestedIteration))
    # returns Total Energy Consumption of a specific carrier in a specific iteration and session
    elif requestedValue == 'energyConsumptionTotal':
        return HttpResponse(funcTotalEnergyConsumption(requestedSession, requestedCarrier, requestedIteration))
    # return Average Acceleration of a specific carrier in a specific iteration and session
    elif requestedValue == 'accelerationAverage':
        return HttpResponse(funcAccelerationAverage(requestedSession, requestedCarrier, requestedIteration))
    else:
        return HttpResponse("Value not defined")


###############################################
######### URL: continuousData.csv #############
###############################################

def continuousData(request):
    # returns a csv File according to the parameters given in the URL
    # I write the function from scratch for simplicity - later merge with db2csv seems reasonable
    response = HttpResponse(content_type='text/csv')
    # the name data.csv is just used by the browser when you query the file directly and want to download it
    response['Content-Disposition'] = 'attachment; filename="data.csv"'

    # extract parameters
    # e.g. for carrier 1, 2 and 5 request position.csv?carrier=1,2,5
    # first split at commas then convert to integers
    # NB: there is no error handling, so make sure you only pass (comma-separated) integers to the function
    requestedCarriers = map(int, request.GET['carriers'].split(','))
    requestedIterations = map(int, request.GET['iterations'].split(','))
    requestedSession = int(request.GET['session'])
    requestedDimension = request.GET['dimension']

    fieldNames = ['timeStamp']
    # create field names for csv file
    # example for carriers 1, 5 and iterations 9, 10
    # timeStamp | c1i9 | c1i10 | c2i9 | c2i10
    for carrier in requestedCarriers:
        for iteration in requestedIterations:
            fieldNames.append('c' + str(carrier) + 'i' + str(iteration))
    writer = csv.DictWriter(response, fieldnames=fieldNames)
    writer.writeheader()

    result = timestampdata.objects.filter(session=requestedSession, carrier__in=requestedCarriers,
                                          iteration__in=requestedIterations).order_by('timeStamp')
    currentTimeStamp = None
    csvRow = {}
    for row in result:
        # we requested data ordered by timestamp, so rows come in blocks with identical timestamp.
        # We iterate through these to fill a the row with this timestamp
        # Once we get a row with a different timeStamp we write the row to the csv file and reset the row
        if currentTimeStamp == None or currentTimeStamp != row.timeStamp:
            if currentTimeStamp != None:
                writer.writerow(csvRow)
            # (re-) set csv-row
            currentTimeStamp = row.timeStamp
            csvRow = {'timeStamp': currentTimeStamp}

        carrier = row.carrier
        iteration = row.iteration
        key = 'c' + str(carrier) + 'i' + str(iteration)
        if requestedDimension == "positionAbsolute":
            csvRow[key] = row.positionAbsolute
        elif requestedDimension == "speed":
            csvRow[key] = row.speed
        elif requestedDimension == "acceleration":
            csvRow[key] = row.acceleration
        elif requestedDimension == "energyConsumption":
            csvRow[key] = row.energyConsumption

    # write last row
    writer.writerow(csvRow)
    return response


###########################################################
######### URL: continuousDataAbsoluteTime.csv #############
###########################################################

# Return absolute time on the X axis and position, speed, acceleration or energy consumption on the y axis depending
# on input parameters
def continuousDataAbsoluteTime(request):
    # returns a csv File according to the parameters given in the URL
    response = HttpResponse(content_type='text/csv')
    # the name data.csv is just used by the browser when you query the file directly and want to download it
    response['Content-Disposition'] = 'attachment; filename="dataAbsoluteTime.csv"'

    # extract parameters
    # e.g. for carrier 1, 2 and 5 request position.csv?carrier=1,2,5
    # first split at commas then convert to integers (not for dimension)
    # NB: there is no error handling, so make sure you only pass (comma-separated) integers to the function
    requestedCarriers = map(int, request.GET['carriers'].split(','))
    requestedIterations = map(int, request.GET['iterations'].split(','))
    requestedSession = int(request.GET['session'])
    requestedDimension = request.GET['dimension']

    fieldNames = ['timeAbsolute']
    # create field names for csv file
    # example for carriers 1, 5 and iterations 9, 10
    # timeStamp | c1i9 | c1i10 | c2i9 | c2i10
    for carrier in requestedCarriers:
        for iteration in requestedIterations:
            fieldNames.append('c' + str(carrier) + 'i' + str(iteration))
    writer = csv.DictWriter(response, fieldnames=fieldNames)
    writer.writeheader()

    result = timestampdata.objects.filter(session=requestedSession, carrier__in=requestedCarriers,
                                          iteration__in=requestedIterations).order_by('timeAbsolute')
    currentTimeStamp = None
    csvRow = {}

    for row in result:
        # we requested data ordered by timestamp, so rows come in blocks with identical timestamp.
        # We iterate through these to fill a the row with this timestamp
        # Once we get a row with a different timeStamp we write the row to the csv file and reset the row
        if currentTimeStamp == None or currentTimeStamp != row.timeAbsolute:
            if currentTimeStamp != None:
                writer.writerow(csvRow)

            # (re-) set csv-row
            currentTimeStamp = row.timeAbsolute
            csvRow = {'timeAbsolute': currentTimeStamp}

        carrier = row.carrier
        iteration = row.iteration
        key = 'c' + str(carrier) + 'i' + str(iteration)
        if requestedDimension == "positionAbsolute":
            csvRow[key] = row.positionAbsolute
        elif requestedDimension == "speed":
            csvRow[key] = row.speed
        elif requestedDimension == "acceleration":
            csvRow[key] = row.acceleration
        elif requestedDimension == "energyConsumption":
            csvRow[key] = row.energyConsumption

    # write last row
    writer.writerow(csvRow)
    return response


###############################################
############ URL: rawData.csv #################
###############################################

def rawData(request):
    # returns a csv File of the raw database tables 
    # parameter table, possible values: timestampdata, iterationdata 
    response = HttpResponse(content_type='text/csv')
    # the name data.csv is just used by the browser when you query the file directly and want to download it
    response['Content-Disposition'] = 'attachment; filename="rawData.csv"'
    writer = csv.writer(response, delimiter=';')

    # extract parameters
    requestedTable = request.GET['table']

    # Returns all data of the timestamp table
    # session, carrier, iteration, timeStamp, drive, positionAbsolute, speed, acceleration, energyConsumption
    if requestedTable == "timestamp":
        result = timestampdata.objects.all()
        for row in result:
            writer.writerow(
                [row.session, row.carrier, row.iteration, row.timeStamp, row.drive, row.positionAbsolute, row.speed,
                 row.acceleration, row.energyConsumption])

    # Returns all data of iteration table
    # session, carrier, iteration, speedAverage, accelerationAverage, energyConsumptionTotal, energyConsumptionAverage
    elif requestedTable == "iteration":
        result = iterationdata.objects.all()
        for row in result:
            writer.writerow([row.session, row.carrier, row.iteration, row.speedAverage, row.accelerationAverage,
                             row.energyConsumptionTotal, row.energyConsumptionAverage])

    # Returns all data of session table
    # Session, FileName, AmountOfCarriers, Status
    elif requestedTable == "sessiondata":
        result = sessiondata.objects.all()
        for row in result:
            writer.writerow([row.session, row.fileName, row.amountOfCarriers, row.status])

    return response


###############################################
############ URL: rawData.json ################
###############################################

def rawDataJson(request):
    # Parameter: Table
    requestedTable = request.GET['table']

    # Defines which table should be returned: SessionData, Iterationdata or TimeStampData
    if requestedTable == "sessiondata":
        data = sessiondata.objects.all()
    elif requestedTable == "iteration":
        data = iterationdata.objects.all()
    elif requestedTable == "timestamp":
        data = timestampdata.objects.all()
    else:
        return HttpResponse("Table doesn't exist")

    # Transpose data to JSON
    json_data = serializers.serialize('json', data)

    # Returns JSON
    return HttpResponse(json_data, content_type='application/json')


###############################################
################# URL: log.txt ################
###############################################

def logs(request):
    # Returns a log file
    # parameter type, possiblie Values: DataProcessing
    requestedType = request.GET['type']

    # Transfer Logfile to String
    with open('/srv/DataProcessing/dataProcessing.log', 'r') as logfile:
        output = logfile.read()

    if requestedType == "DataProcessing":
        response = HttpResponse(output, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename="Log.txt"'
        return response


def deleteDatabaseValues(request):
    # deletes all values of a particular table of the database
    # parameter: table
    # Transform request to variable
    requestedTable = request.GET['table']

    # parameter 'iteration' deletes all values in iterationdata and returns OK
    if requestedTable == 'iteration':
        iterationdata.objects.all().delete()
        return HttpResponse('OK')
    # parameter 'timestamp' deletes all values in timestampdata and returns OK
    elif requestedTable == 'timestamp':
        timestampdata.objects.all().delete()
        return HttpResponse('OK')
    # parameter 'sessiondata' deletes all values in sessiondata and returns OK
    elif requestedTable == 'sessiondata':
        sessiondata.objects.all().delete()
        return HttpResponse('OK')
    # parameter 'all' deletes all values in sessiondata, iterationdata and timestampdata and returns OK
    elif requestedTable == 'all':
        iterationdata.objects.all().delete()
        timestampdata.objects.all().delete()
        sessiondata.objects.all().delete()
        return HttpResponse('OK')
    else:
        # Any Other parameter returns 'FAIL'
        return HttpResponse('FAIL')


###############################################
######## URL: simulation.files ################
###############################################

def simulationFiles(request):
    # reads out all files in the InitialData - Folder
    files = dataProcessingFunctions.checkForCSVFilesInFolder('/srv/DataProcessing/InitialData')

    # Defines FileNamesAsString
    fileNamesAsString = ""

    # Adds all filenames to the string if it is isn't a modified file that is created during a simulation run.
    for file in files:
        if not '_modified.csv' in file:
            fileNamesAsString = fileNamesAsString + file + ','

    # returns the string
    return HttpResponse(fileNamesAsString[0: len(fileNamesAsString) - 1])


###############################################
######## URL: simulation.reset ################
###############################################

def resetSimulation(request):
    # Deletes all DatabaseValues and sets the Session in the cofigFile to Zero

    # Deletes all Values from iterationdata
    iterationdata.objects.all().delete()
    # Deletes all Values from timestampdata
    timestampdata.objects.all().delete()
    # Deletes all Values from sessiondata
    sessiondata.objects.all().delete()

    dataProcessingFunctions.updated_config('Simulation', 'session', 1)

    return HttpResponse('OK')


###############################################
######## URL: simulation.start ################
###############################################

def startSimulation(request):
    # Sets all values that are needed to start the simulation and starts the simulation

    # Requested Parameters:
    # Waittimes, FileName, KeepEveryXRows, AmountOfCarriers
    requestedwtSimulation = request.GET['wtSimulation']
    requestedwtFirstDataLoad = request.GET['wtFirstDataload']
    requestedwtDataReload = request.GET['wtDataReload']
    requestedAmountOfCarriers = request.GET['amountOfCarriers']
    requestedfileName = request.GET['fileName']
    requestedKeepEveryxRows = request.GET['keepEveryXRows']

    # Sets Values in ConfigFile in DataProcessingFolder
    # AmountOfCarriers
    dataProcessingFunctions.updated_config('Simulation', 'amount_of_carriers', requestedAmountOfCarriers)
    # Waittime in the Compression and divides the value by 1000 because it are ms not s
    dataProcessingFunctions.updated_config('Simulation', 'waittime_compression', int(requestedwtSimulation) / 1000)
    # Waittime for the first dataload of WriteCarrierDataToDataBase
    dataProcessingFunctions.updated_config('Simulation', 'waittime_first_dataload', requestedwtFirstDataLoad)
    # Waittime for the data reload of WriteCarrierDataToDataBase
    dataProcessingFunctions.updated_config('Simulation', 'waittime_data_reload', requestedwtDataReload)
    # FileName that should be imported
    dataProcessingFunctions.updated_config('Simulation', 'name_of_imported_file', requestedfileName)
    # KeepEveryXRows to determine the compressionRate
    dataProcessingFunctions.updated_config('Simulation', 'keep_every_x_rows', requestedKeepEveryxRows)

    # Starts both DataProcessing Scripts in the background
    subprocess.Popen(["python", "/srv/DataProcessing/compressInitialData.py"], cwd='/srv/DataProcessing')
    subprocess.Popen(["python", "/srv/DataProcessing/writeCarrierDataToDataBase.py"], cwd='/srv/DataProcessing')

    # Returns Running after Success
    return HttpResponse('Running')


###############################################
#### URL: averageEnergyConsumption.csv #######
###############################################

def averageEnergyConsumption(request):
    # Provides last 10 iterations  for the AverageEnergyConsumptionChart
    # parameters: session, carriers, dimension,  type
    requestedSession = request.GET['session']
    requestedCarriers = request.GET['carriers']
    requestedDimension = request.GET['dimension']
    requestedType = request.GET['type']

    # Parsing Carriers because the the different carriers are given comma seperated
    carriers = requestedCarriers.split(',')

    # Creating response with attachment as data.csv
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="data.csv"'
    # Dygraph can just handle , - seperated csv files
    writer = csv.writer(response, delimiter=',')

    # determine max iteration of all requested carriers
    maxIterationOfAllCarriers = 0
    for carrier in carriers:
        if funcMaxIteration(requestedSession, carrier) > maxIterationOfAllCarriers:
            maxIterationOfAllCarriers = funcMaxIteration(requestedSession, carrier)

    # TODO: Make last10 flexible. So if last3 are requested, return last 3

    # Determines the startIteration that should be provided in the .csv file
    if requestedType == "last10":
        # If the last 10 iterations are requested, substract 10 from maxIterationOfAllCarriers if
        # maxIterationOfAllCarriers is larger then 10, else startIteration is 1
        if maxIterationOfAllCarriers > 9:
            startIterationOfAllCarriers = maxIterationOfAllCarriers - 9
        else:
            startIterationOfAllCarriers = 1
    elif requestedType == "last3":
        if maxIterationOfAllCarriers > 2:
            startIterationOfAllCarriers = maxIterationOfAllCarriers - 2
        else:
            startIterationOfAllCarriers = 1
    elif requestedType == "all":
        # If all iterations are requested iterating should start at 1
        startIterationOfAllCarriers = 1
    else:
        # If neither 'all' or 'last' return "Wrong Type Selected'
        return HttpResponse('Wrong Type Selected')

    # write first row of iteration.
    # Iterations, Carrier 0, Carrier 1, Carrier X
    firstrow = ['Iteration']
    for carrier in carriers:
        firstrow.append('Carrier ' + carrier)
    writer.writerow(firstrow)

    # Writes rest of the csv file
    for iteration in range(startIterationOfAllCarriers, maxIterationOfAllCarriers):
        # Creates a list with all values.
        # first value is "Iteration No"
        rowOfValues = [iteration]
        # Iterates all carriers
        for carrier in carriers:
            #  Appends result of function funcTotalEnergyConsumption to the list
            if requestedDimension == 'energyConsumptionTotal':
                rowOfValues.append(funcTotalEnergyConsumption(requestedSession, carrier, iteration))
            # Appends result of function funcSpeedAverage to the list
            elif requestedDimension == 'speedAverage':
                rowOfValues.append(funcTotalEnergyConsumption(requestedSession, carrier, iteration))
            # Appends result of function funcAccelerationAverage to the list
            elif requestedDimension == 'accelerationAverage':
                rowOfValues.append(funcAccelerationAverage(requestedSession, carrier, iteration))
            # Appends result of function funcAverageEnergyConsumption to the list
            elif requestedDimension == 'energyConsumptionAverage':
                rowOfValues.append(funcAverageEnergyConsumption(requestedSession, carrier, iteration))
            # any other paramater returns 'no such paramater defined'
            else:
                return HttpResponse('No such paramter defined')

        # Writes the row
        writer.writerow(rowOfValues)

    # Returns csv file
    return response


###############################################
##### URL: percentages_creeping.csv ###########
###############################################

def percentage_creeping(request):
    # Provides a csv file of percent energy consumption from first to last iteration
    # parameter requested Session
    requestedSession = request.GET['session']

    # Creating response with attachment as data.csv
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="data.csv"'
    # Dygraph can just handle , - seperated csv files
    writer = csv.writer(response, delimiter=',')

    # Reads out amountOfCarriers for requested Session
    amountOfCarriers = funcAmountOfCarriers(requestedSession)

    # Initializes list for first and second row
    firstRow = []
    secondRow = []

    for carrier in range(1, amountOfCarriers + 1):
        # Appends Carrier + No to the first row
        firstRow.append('Carrier' + str(carrier))
        # Appends the percentage for each carrier (EnergyConsumption last iteration/energyConsumption first iteration)
        secondRow.append(funcPercentCreeping(requestedSession, carrier))

    # Writes CSV - File
    writer.writerow(firstRow)
    writer.writerow(secondRow)

    # Returns CSV-File
    return response


###############################################
######### URL: percentages_cont.csv ###########
###############################################

def percentage_cont(request):
    # Provides a csv file of percent energy consumption from first to last iteration
    # parameter requested Session
    requestedSession = request.GET['session']

    # Creating response with attachment as data.csv
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="data.csv"'
    # Dygraph can just handle , - seperated csv files
    writer = csv.writer(response, delimiter=',')

    # Reads out amountOfCarriers for requested Session
    amountOfCarriers = funcAmountOfCarriers(requestedSession)

    # Initializes list for first and second row
    firstRow = []
    secondRow = []

    for carrier in range(1, amountOfCarriers + 1):
        # Appends Carrier + No to the first row
        firstRow.append('Carrier' + str(carrier))
        # Appends the percentage for each carrier (EnergyConsumption last iteration/energyConsumption first iteration)
        secondRow.append(funcPercentCont(requestedSession, carrier))

    # Writes CSV - File
    writer.writerow(firstRow)
    writer.writerow(secondRow)

    # Returns CSV-File
    return response


###############################################
######### URL: fileUpload.html ################
###############################################

# disables djangos build in cross site request forgery protection mechanism
@csrf_exempt
def fileUpload(request):
    fileName = request.POST['fileName']
    file = request.FILES['file']
    
    # check if file with that name already exists
    if sessiondata.objects.filter(fileName=fileName).exists():
        # there is certainly a more user-friendly way to handle this but for now it should be fine
        return HttpResponse(status=409)

    # no file with the given name exists (according to the database), write it to the directory
    with open('/srv/DataProcessing/InitialData/' + fileName + '.csv', 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    # maybe add new session to session database here
    # so far the session is added only after the corresponding simulation has been executed
    
    return HttpResponse(status=205)


###############################################
######### URL: simulation.running #############
###############################################

def simulationRuns(request):
    # Depending on if a modified csv file is in the the InitialData Folder it returns true for running or not

    # reads out all files in the InitialData - Folder
    files = dataProcessingFunctions.checkForCSVFilesInFolder('/srv/DataProcessing/InitialData')

    # Return true if a modified csv file is found
    for file in files:
        if '_modified.csv' in file:
            return HttpResponse(True)

    # else returns false
    return HttpResponse(False)
