# @author AMOSus (Daniel)
# @author inkibus (Rene)

# This script is a simple simulator of RealTimedata to enable the Algorythm to compress the Data in a proper way
# Input: CSV file with the following structure (ms, energy1, ..., energyX, pos1,...,posX) (x = Amount of Drives)
# The script calls depending on the amount of drives and waittime the CompressingAlgorythm all x seconds

#TODO: add up the energy cosumptio instead of averaging it

# Imports Pandas for Data handling
import pandas as pd
# Imports OS for Operating System independent absolute filepaths
import os
# Imports Pandas for Data handling
import numpy as np
# Imports sleep for sleeping
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
# This is where all the data goes before exporting to CSV
# carrierData[carrier number][time = 0, pos = 1, energy consumption = 2][position of array]
carrierData = np.zeros((AMOUNT_OF_CARRIERS, 3, 100))
# Here is stored in which row the last entry of carrier data was made for every carrier
currentPositionAtCarrierData = np.zeros(AMOUNT_OF_CARRIERS)
# Saves the last position on the drive of every carrier
lastPositionOfCarrier = np.zeros(AMOUNT_OF_CARRIERS)
# Number of complete runs through the system
runNumber = 0
# The amount of carriers who entered drive 1 (Therefore starting with carrier 1) in the current run
carriersThroughTheSystem = 1


# Main data processing script. Gets input data of drives and maps it to the carries and saves them as CSV files
def processData(INPUT):
    # Ensures that new Run is initialized before referencing
    global runNumber
    # Ensures that carrier Data is called from global variables
    global carrierData
    # TODO maybe Save all INPUT values here to a local variable and use those throughout the algorithm

    print " "
    time = INPUT[0]
    print "Time      " + str(time)
    position = INPUT[3]
    print "Position  " + str(position)
    energy = INPUT[2]
    print "Energy    " + str(energy)

    # If the line has just started, then the first carrier enters the first drive
    if runNumber == 0:
        print "line has just started: Carrier 1 at Drive 1"
        runNumber = 1
        driveXHasCarrier[0] = 1

    drive = int(INPUT[1])
    print " "
    print "Drive     " + str(drive)
    carrier = int(driveXHasCarrier[drive - 1])
    print "Carrier   " + str(carrier)

    # If the current drive doesnt have a carrier, it cannot be mapped
    if driveXHasCarrier[drive - 1] == 0:
        print "Drive " + str(drive) + " doesn't have a carrier, the data is deleted"
        # TODO maybe save the amount of data that is being deleted
        return

    # If the timestamp is the same as in the previous run, the data is not recorded
    # This only happens when pushing carries which should not happen in the first place
    if time == carrierData[carrier - 1][0][currentPositionAtCarrierData[carrier - 1] - 1]:
        print "Timestamp is the same as before, the data is deleted"
        return

    # If position is zero and if position is lower than it was in the previous run
    if position == 0 and (position < lastPositionOfCarrier[carrier - 1]):
        evaluateDriveReset(drive, carrier)

    # Ensures enough space in the array
    ensureEnoughSpaceInCarrierData(carrier)

    # Transfer time in ms
    carrierData[carrier - 1][0][currentPositionAtCarrierData[carrier - 1]] = time
    # Transfer position
    carrierData[carrier - 1][1][currentPositionAtCarrierData[carrier - 1]] = position
    lastPositionOfCarrier[carrier - 1] = position
    # Transfer energy consumption
    carrierData[carrier - 1][2][currentPositionAtCarrierData[carrier - 1]] = energy
    # So that next time the next row will be filled with data
    currentPositionAtCarrierData[carrier - 1] += 1

    return


# If a drive reset its position to 0, it takes a new carrier
def evaluateDriveReset(drive, carrier):
    print "Drive " + str(drive) + " restarted"

    # If the carrier is at the last drive, the run can be completed
    if drive == AMOUNT_OF_DRIVES:
        completeRun(drive, carrier)
        # If all carriers went through the drives, the run is complete and run number 2 can start
        if carrier == AMOUNT_OF_CARRIERS:
            global runNumber
            runNumber += 1

    print "currently Drive X has Carrier"
    print driveXHasCarrier
    # the Carrier leaves the current drive
    driveXHasCarrier[drive - 1] = 0
    lastPositionOfCarrier[carrier - 1] = 0

    # The carrier moves to the next drive
    # Check if there is a next drive
    if drive < AMOUNT_OF_DRIVES:
        # Check if next drive is empty
        if driveXHasCarrier[drive - 1 + 1] == 0:
            # Give the next drive the current carrier
            driveXHasCarrier[drive - 1 + 1] = carrier
        else:
            print "Carrier " + str(carrier) + " wants to go to drive " + str(drive + 1) + " ,but there is carrier " \
                  + str(driveXHasCarrier[drive - 1 + 1]) + " on there"
            evaluateDriveReset(drive + 1, driveXHasCarrier[drive - 1 + 1])
            driveXHasCarrier[drive - 1 + 1] = carrier

    # If the current drive is drive 1, then a new carrier is pulled onto the drive 1
    if drive == 1:
        print "new carrier gets pulled"
        # Ensures that the global variable is used
        global carriersThroughTheSystem
        # One more carrier passed through the entrance of the system
        carriersThroughTheSystem += 1
        # The new carrier enters the drive and is 1 number bigger than the highest one in the production line
        # But if all the carriers already were on the system
        # The run number is increased
        # And carrier 1 is on drive 1 again
        if carriersThroughTheSystem > AMOUNT_OF_CARRIERS:
            carriersThroughTheSystem = 1
            driveXHasCarrier[drive - 1] = carriersThroughTheSystem
        else:
            driveXHasCarrier[drive - 1] = carriersThroughTheSystem

    print "After the carriers have moved "
    print driveXHasCarrier
    # If the last carrier completed the run, run number +1



# If a carrier leaves the last drive, the data has to be compressed and the CSV file has to be saved
def completeRun(drive, carrier):
    print carrierData
    compressData(drive, carrier)
    print carrierData

    exportCSV(carrier)

    clearCarrierData(carrier)

    # Set the current position that is being filled to 0 so that the array can be filled again
    currentPositionAtCarrierData[carrier - 1] = 0

# Compresses the data, so that only every X-th (KEEP_EVERY_X_ROW) is kept in the data
# Example: rows: 1,2,3,4,5,6 --> compressData with KEEP_EVERY_X_ROW == 2 --> rows: 1,3,5
def compressData(drive, carrier):
    print "The drive "
    print drive
    print "reset its position"
    print " "

    # the Value where the average is built
    valueAverage = 0
    # iterates through all the carrier data entries that have been made up to this point
    # the if else is just there to catch an out of bounds exception where the currentPosition is bigger than the array size of carrierData[2]
    # statement: do a if x < y else b ----> does a if x < y .. otherwise it does b
    print "range: " + str(int(currentPositionAtCarrierData[carrier - 1] if (
    currentPositionAtCarrierData[carrier - 1] - 1 < int(carrierData.shape[2])) else int(carrierData.shape[2]) - 1))
    for i in range(0, int(currentPositionAtCarrierData[carrier - 1] if (
                    currentPositionAtCarrierData[carrier - 1] - 1 < int(carrierData.shape[2])) else int(
        carrierData.shape[2]) - 1)):

        print "i: " + str(i)
        # Saves the first x numbers to row 0, then the second x numbers to row 1 and so on
        saveTo = int(i / KEEP_EVERY_X_ROW)
        print "saveTo " + str(saveTo)

        # Time and position will just be overwritten so that it has 1,X,2X,3X,4X from KEEP_EVERY_X_ROW
        if int(i % KEEP_EVERY_X_ROW) == 0:
            carrierData[carrier - 1][0][saveTo] = carrierData[carrier - 1][0][i]
            carrierData[carrier - 1][1][saveTo] = carrierData[carrier - 1][1][i]
            carrierData[carrier - 1][2][saveTo] = carrierData[carrier - 1][2][i]
        else:
            # Test, so that the value at saveTo is not added to itself
            if saveTo != i:
                # Add the energy to calculate average
                carrierData[carrier - 1][2][saveTo] += carrierData[carrier - 1][2][i]

        print str(carrierData[carrier - 1][0][saveTo]) + "    " \
              + str(carrierData[carrier - 1][1][saveTo]) + "    " \
              + str(carrierData[carrier - 1][2][saveTo])

        # WORKS
        # if my current row is bigger than what the largest row to keep would be then empty that row
        if i >= 1 + int((currentPositionAtCarrierData[carrier - 1] - 1) / float(KEEP_EVERY_X_ROW)):
            print "deleting row " + str(i)
            carrierData[carrier - 1][0][i] = 0
            carrierData[carrier - 1][1][i] = 0
            carrierData[carrier - 1][2][i] = 0

        # If all the X amount lines are added up they then can be averaged
        if i != 0 and (i + 1) % KEEP_EVERY_X_ROW == 0:
            # Make sure that the nex one wouldn't be saved to the same one, so the adding up is complete and the
            # averaging can begin
            assert saveTo != int(i + 1 / KEEP_EVERY_X_ROW)

            print "carrierData[carrier - 1][2][saveTo] " + str(carrierData[carrier - 1][2][saveTo])
            print "carrierData[carrier - 1][2][saveTo] / KEEP_EVERY_X_ROW " + str(
                carrierData[carrier - 1][2][saveTo] / KEEP_EVERY_X_ROW)

            carrierData[carrier - 1][2][saveTo] = carrierData[carrier - 1][2][saveTo] / KEEP_EVERY_X_ROW

        # If its the last row that is being iterated, but the average is not yet calculated
        # So if 199 are done and ever 10th row is kept, then 9 more rows need averaging in the end
        else:
            print "Last row reached, summing up last row"
            if i == (
                currentPositionAtCarrierData[carrier - 1] - 1 if currentPositionAtCarrierData[carrier - 1] - 1 < int(
                    carrierData.shape[2]) else int(carrierData.shape[2]) - 1):
                numberOfRowsLeft = int(i % KEEP_EVERY_X_ROW) if int(i % KEEP_EVERY_X_ROW) != 0 else 1
                carrierData[carrier - 1][2][saveTo] = carrierData[carrier - 1][2][saveTo] / numberOfRowsLeft

# Exports the table of the carrier to a CSV file
def exportCSV(carrier):
    print "Exporting: "
    print carrierData[carrier - 1]
    filename = "Carrier_" + str(int(carrier)) + "_Run_" + str(int(runNumber)) + ".csv"
    print "filename " + str(filename)
    firstRow = findFirstRowInCarrierData(carrier)
    print "first Row " + str(firstRow)
    lastRow = int((currentPositionAtCarrierData[carrier - 1] - 1) / KEEP_EVERY_X_ROW)
    print "last Row " + str(lastRow)
    export = np.transpose(carrierData[carrier - 1][:,firstRow:lastRow])
    print "export"
    print export

    np.savetxt(filename, export,  fmt='%0.5f', delimiter=';', newline='\n', header='ms;pos;energy', footer='', comments='# ')
    #np.savetxt(filename, np.transpose(carrierData[carrier - 1]), fmt='%0.5f', delimiter=';', newline='\n',
     #          header='ms;pos;energy', footer='', comments='# ')

# Finds the first row of the array that will be exported as CSV, where pos and energy consumption != 0
def findFirstRowInCarrierData(carrier):
    firstRow = 0
    for i in range(0, int(carrierData.shape[2]) - 1):
        if (carrierData[carrier - 1][1][i] == 0) and (carrierData[carrier - 1][2][i] == 0):
            firstRow = i
        else:
            return firstRow
    return firstRow

# Clear the data array
def clearCarrierData(carrier):
    for i in range(0, int(carrierData.shape[2]) - 1):
        carrierData[carrier - 1][0][i] = 0
        carrierData[carrier - 1][1][i] = 0
        carrierData[carrier - 1][2][i] = 0

# Ensures enough space in the carrier data array
def ensureEnoughSpaceInCarrierData(carrier):
    global carrierData
    if currentPositionAtCarrierData[carrier - 1] >= carrierData.shape[2]:
        carrierData = np.resize(carrierData,
                                (int(carrierData.shape[0]), int(carrierData.shape[1]), int(carrierData.shape[2] * 2)))

#
# Start of the Script
#

# Loads Csv into a pandas DataFrame
InitialData = pd.read_csv(DATA_PATH, DATA_SEPARATOR)

a = InitialData.iterrows()

# Iterates each row and afterwards each drive
# Calls compressData with a pd.Series. The values are:
# ms, No. of Drive, Energy Consumption, Position
for index, row in InitialData.iterrows():
    for i in range(0, AMOUNT_OF_DRIVES):
        # TODO For me (RENE) just an array makes more sense than a Series here
        processData(pd.Series([row['ms'], i + 1, row['energy' + str(i + 1)], row['pos' + str(i + 1)]]))
    sleep(WAIT_TIME_IN_SECONDS)
# print carrierData
