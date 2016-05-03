# @author AMOSus (Daniel)
# @author inkibus (Rene)
# TODO refactoring
# TODO clean the code (didnt have time for that)
# TODO test with working dummy data and fix bugs

# This script is a simple simulator of RealTimedata to enable the Algorythm to compress the Data in a proper way
# Input: CSV file with the following structure (ms, energy1, ..., energyX, pos1,...,posX) (x = Amount of Drives)
# The script calls depending on the amount of drives and waittime the CompressingAlgorythm all x seconds

# Imports Pandas for Datahandling and Sleep for waiting
import pandas as pd
# Imports OS for Operating System independent absolute filepaths
import os
import numpy as np
from time import sleep

# Constants
# WAIT_TIME_IN_SECONDS: Time the script should wait until it calls the function again (in seconds)
WAIT_TIME_IN_SECONDS = 0.001
# AMOUNT_OF_DRIVES: How many Drives are producing data
AMOUNT_OF_DRIVES = 3
# AMOUNT_OF_CARRIERS: How many Carriers are in the system
AMOUNT_OF_CARRIERS = 3
# DATA_PATH = Path of the CSV - File that should be simulated
# #UPDATE:(creates now an OS independent file path to the daten_cleaning.csv)
DATA_PATH = os.path.abspath(os.path.join("data", "testData_Rene.csv"))
# DATA_SEPARATOR: Separator of the CSV-File
DATA_SEPARATOR = ';'
# Every X th row of the data is kept and averagedx
KEEP_EVERY_X_ROW = 2

# Variables
# linearDrivesData = np.zeros((AMOUNT_OF_DRIVES,3,100))
# currentPositionAtDrive = np.zeros(AMOUNT_OF_DRIVES)
driveXHasCarrier = np.zeros(AMOUNT_OF_DRIVES)
carrierData = np.zeros((AMOUNT_OF_CARRIERS, 3, 100))
currentPositionAtCarrier = np.zeros(AMOUNT_OF_CARRIERS)
# carrierAtPos = np.zeros(AMOUNT_OF_CARRIERS)
runNumber = 0
#The amount of carriers who passed drive 1
carriersThroughTheSystem = 0


def compressData(INPUT):
    #TODO alle variablen am anfang anlegen dass es evtl auch geaendert werden kann (also nochmal lokal speichern),
    print "Input"
    print INPUT
    print " "

    drive = int(INPUT[1])

    print "Drive"
    print drive
    print " "

    # Ensures that new Run is initialized before referencing
    global runNumber

    # Ensures that carrier Data is called from global variables
    global carrierData
    # If the line has just started, then the first carrier enters the first drive
    # if driveXHasCarrier == np.zeros(AMOUNT_OF_CARRIERS): old version
    if runNumber == 0:
        print "line has just started: Carrier 1 at Drive 1"
        print " "

        runNumber += 1
        driveXHasCarrier[0] = 1

    carrier = int(driveXHasCarrier[drive - 1])
    print "Carrier"
    print carrier
    print " "

    # If the current drive doesnt have a carrier, it cannot be mapped
    if driveXHasCarrier[drive - 1] == 0:
        print "the Drive doesnt have a carrier, the data is deleted"
        # TODO maybe save the amount of data that is being deleted
        return

    # If the current Drive position has is 0 and was not 0 before, then the drive reset itself.
    # This means that now the data can be compressed, then the CSV file can be saved.
    # Also the current linearDrivesData should be cleared for that drive.
    if INPUT[3] == 0 and (INPUT[3] < carrierData[carrier - 1][1][currentPositionAtCarrier[carrier - 1] - 1]):
        print "The drive "
        print drive
        print "reset its position"
        print " "

        print carrierData

        # the Value where the average is built
        valueAverage = 0
        # iterates through all the carrier data entries that have been made up to this point
        # the if else is just there to catch an out of bounds exception where the currentPosition is bigger than the array size of carrierData[2]
        # statement: do a if x < y else b ----> does a if x < y .. otherwise it does b
        for i in range(0, int(currentPositionAtCarrier[carrier - 1] - 1 if (currentPositionAtCarrier[carrier - 1] - 1 < int(carrierData.shape[2])) else int(carrierData.shape[2]) - 1)):
            # Saves the first x numbers to row 0, then the second x numbers to row 1 and so on
            saveTo = int(i / KEEP_EVERY_X_ROW)

            # Adding the values to the current sport
            # for example add the values of carrierData points 1,2,3,4,5,6,7,8,9 to the value of carrierData point 0
            # Except the ti,e. The time will directly be overwritten so that it
            # For the time and the position only the last value needs to be saved thats why it needs to be overwritten
            carrierData[carrier - 1][0][saveTo] = carrierData[carrier - 1][0][i]
            carrierData[carrier - 1][1][saveTo] = carrierData[carrier - 1][1][i]
            # Test, so that the value at saveTo is not added to itself
            if saveTo != i:
                carrierData[carrier - 1][2][saveTo] += carrierData[carrier - 1][2][i]

            # If all the X amount lines are added up they then can be averaged
            if i != 0 and (i + 1) % KEEP_EVERY_X_ROW == 0:
                # Make sure that the nex one wouldn't be saved to the same one, so the adding up is complete and the
                # averaging can begin
                assert saveTo != int(i + 1 / KEEP_EVERY_X_ROW)

                carrierData[carrier - 1][0][saveTo] = (saveTo * KEEP_EVERY_X_ROW) + (KEEP_EVERY_X_ROW / 2)
                carrierData[carrier - 1][1][saveTo] = carrierData[carrier - 1][1][saveTo] / KEEP_EVERY_X_ROW
                carrierData[carrier - 1][2][saveTo] = carrierData[carrier - 1][2][saveTo] / KEEP_EVERY_X_ROW
                continue

            # If its the last row that is being iterated, but the average is not yet calculated
            # So if 199 are done and ever 10th row is kept, then 9 more rows need averaging in the end
            if i == currentPositionAtCarrier[carrier - 1] - 1 if currentPositionAtCarrier[carrier - 1] - 1 < int(
                    carrierData.shape[2]) else int(carrierData.shape[2]) - 1:
                numberOfRowsLeft = int(i % KEEP_EVERY_X_ROW)
                carrierData[carrier - 1][0][saveTo] = saveTo * KEEP_EVERY_X_ROW + numberOfRowsLeft / 2
                carrierData[carrier - 1][1][saveTo] = carrierData[carrier - 1][1][saveTo] / numberOfRowsLeft
                carrierData[carrier - 1][2][saveTo] = carrierData[carrier - 1][2][saveTo] / numberOfRowsLeft
                continue

        print carrierData

        filename = "Carrier_" + str(carrier) + "_Run_" + str(runNumber) + ".csv"
        np.savetxt(filename, np.transpose(carrierData[carrier - 1]), fmt='%0.5f', delimiter=';', newline='\n', header='ms;energy;pos', footer='', comments='# ')

        # Clear the data array
        for i in range(0, int(carrierData.shape[2]) - 1):
            carrierData[carrier - 1][0][i] = 0
            carrierData[carrier - 1][1][i] = 0
            carrierData[carrier - 1][2][i] = 0

        # Set the current row that is being filled to 0 so that the array can be filled again
        currentPositionAtCarrier[carrier - 1] = 0

        # Iterate the carrier to the next drive
        driveXHasCarrier[drive - 1] = 0
        # Check if there is a next drive and if its empty
        # TODO IMPORTANT what if the next drive is not yet empty? then the algorithm needs to take care of that first before putting the carrier there
        if drive < AMOUNT_OF_DRIVES and int(driveXHasCarrier[drive - 1]) == 0:
            # - 1 because of the array bounds from 0 to AMOUNT_OF_DRIVES and +1 because the next drive is selected
            driveXHasCarrier[drive - 1 + 1] = carrier

        # If the drive is drive 1, then a new carrier is pulled onto the drive 1
        if drive == 1:
            global carriersThroughTheSystem
            #One more carrier passed through the entrance of the system
            carriersThroughTheSystem += 1
            # The new carrier enters the drive and is 1 number bigger than the highest one in the production line
            # But if all the carriers already were on the system
            # The run number is increased
            # And carrier 1 is on drive 1 again
            if carriersThroughTheSystem > AMOUNT_OF_CARRIERS:
                carriersThroughTheSystem = 1
                driveXHasCarrier[drive - 1] = carriersThroughTheSystem
                runNumber += 1
            else:
                driveXHasCarrier[drive - 1] = carriersThroughTheSystem

            # Ensures enough space in the array

    if currentPositionAtCarrier[carrier - 1] >= carrierData.shape[2]:
        carrierData = np.resize(carrierData, (
        int(carrierData.shape[0]), int(carrierData.shape[1]), int(carrierData.shape[2] * 2)))

    # Transfer time in ms
    carrierData[carrier - 1][0][currentPositionAtCarrier[carrier - 1]] = INPUT[0]
    # Transfer position
    carrierData[carrier - 1][1][currentPositionAtCarrier[carrier - 1]] = INPUT[3]
    # Transfer energy consumption
    carrierData[carrier - 1][2][currentPositionAtCarrier[carrier - 1]] = INPUT[2]
    # So that next time the next row will be filled with data
    currentPositionAtCarrier[carrier - 1] += 1

    return


# Loads Csv into a pandas DataFrame
InitialData = pd.read_csv(DATA_PATH, DATA_SEPARATOR)

a = InitialData.iterrows()

# Iterates each row and afterwards each drive
# Calls compressData with a pd.Series. The values are:
# ms, No. of Drive, Energy Consumption, Position
for index, row in InitialData.iterrows():
    for i in range(0, AMOUNT_OF_DRIVES):
        # TODO For me (RENE) just an array makes more sense than a Series here
        compressData(pd.Series([row['ms'], i + 1, row['energy' + str(i + 1)], row['pos' + str(i + 1)]]))
    sleep(WAIT_TIME_IN_SECONDS)
print carrierData
