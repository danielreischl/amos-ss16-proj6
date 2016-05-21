# @author AMOSus (Daniel)
# @author inkibus (Rene)

# TODO: Remove the position on Drive everywhere (all variables, CSV output), since it cannot be calculated anymore.
# TODO: Fix the bug with having some odd timestamps in the exported csv files (The point above may resolve this issue)
# TODO: Heavy refactoring and rework comments for readability and maintainability
# TODO: Now some kind of measure for flexibility can be implemented and calculated here!

# This script is a simple simulator of RealTimedata to enable the Algorythm to compress the Data in a proper way
# Input: CSV file with the following structure (ms, energy1, ..., energyX, pos1,...,posX) (x = Amount of Drives)
# The script calls depending on the amount of drives and waittime the CompressingAlgorythm all x seconds

# Imports Pandas for Data handling
from __future__ import print_function
import pandas as pd
# Imports OS for Operating System independent absolute file paths
import os
# Imports Pandas for Data handling
import numpy as np
# Imports sleep for sleeping
from time import sleep
# Imports setConstants to maintain all constants on one place
import setConstants
# Import glob to enable the search in a folder
import glob
# Imports sys to terminate the function
import sys
# Imports Csv to Manipulate Initial CSV-File
import csv
# Imports Logging to Log File
import logging

# Constants
# WAIT_TIME_IN_SECONDS: Time the script should wait until it calls the function again (in seconds)
WAIT_TIME_IN_SECONDS = setConstants.WAIT_TIME_IN_SECONDS_DPPY
# Input file names of data here
DATA_FILE_NAMES = []
# AMOUNT_OF_CARRIERS: How many Carriers are in the system
AMOUNT_OF_CARRIERS = setConstants.AMOUNT_OF_CARRIERS
# DATA_SEPARATOR: Separator of the CSV-File
DATA_SEPARATOR = setConstants.CSV_SEPARATOR
# Every X th row of the data is kept and averagedx
KEEP_EVERY_X_ROW = 100
# Current Session
SESSION = setConstants.SESSION

# Main data processing script. Gets input data of drives and maps it to the carries and saves them as CSV files
def processData(INPUT):

    # Ensures that new Run is initialized before referencing
    global runNumber
    # Ensures that carrier Data is called from global variables
    global carrierData

    time = int(INPUT[0])
    drive = int(INPUT[1])
    position = INPUT[2]
    energy = INPUT[3]

    # If the line has just started, then the first carrier enters the first drive
    if runNumber == 0:
        print ("line has just started: Carrier 1 at Drive 1")
        runNumber = 1
        driveXHasCarrier[0] = 1

    carrier = int(driveXHasCarrier[drive - 1])

    # If the current drive doesnt have a carrier, it cannot be mapped
    if driveXHasCarrier[drive - 1] == 0:
        #print ("Drive " + str(drive) + " doesn't have a carrier, the data is deleted")
        return

    # If the timestamp is the same as in the previous run, the data is not recorded
    # This only happens when pushing carries which should not happen in the first place
    if time == carrierData[carrier - 1][0][currentPositionAtCarrierData[carrier - 1] - 1]:
        #print ("Timestamp is the same as before, the data is deleted")
        return



    # If position is zero and if position is lower than it was in the previous run
    if position == 0 and lastPositionOfCarrier[carrier - 1] != 0:

        print (" ")
        print ("Drive     " + str(drive))
        print ("Carrier   " + str(carrier))
        print ("Time      " + str(time))
        print ("Position  " + str(position))
        print ("Energy    " + str(energy))

        evaluateDriveReset(drive, carrier)
        processData([time, drive, position, energy])
        return

    # Ensures enough space in the array
    ensureEnoughSpaceInCarrierData(carrier)

    #positionAbsolute = (drive - 1) * setConstants.DRIVE_LENGTH + position
    #print ("Position Absolute:    " + str(positionAbsolute))

    # Transfer time in ms
    carrierData[carrier - 1][0][currentPositionAtCarrierData[carrier - 1]] = time
    # Transfer position
    carrierData[carrier - 1][1][currentPositionAtCarrierData[carrier - 1]] = position

    carrierData[carrier - 1][2][currentPositionAtCarrierData[carrier - 1]] = position
    lastPositionOfCarrier[carrier - 1] = position

    # Transfer energy consumption
    carrierData[carrier - 1][3][currentPositionAtCarrierData[carrier - 1]] = energy

    # So that next time the next row will be filled with data
    currentPositionAtCarrierData[carrier - 1] += 1

    return


# If a drive reset its position to 0, it takes a new carrier
def evaluateDriveReset(drive, carrier):
    print("Before moving carriers ")
    print(driveXHasCarrier)

    # the Carrier leaves the current drive
    driveXHasCarrier[drive - 1] = 0
    lastPositionOfCarrier[carrier - 1] = 0

    print ("Drive " + str(drive) + " restarted")

    # If the carrier is at the last drive, the run can be completed
    if drive == amountOfDrives:
        completeRun(drive, carrier)
        # If all carriers went through the drives, the run is complete and run number 2 can start
        if carrier == AMOUNT_OF_CARRIERS:
            global runNumber
            runNumber += 1

    # The carrier moves to the next drive
    # Check if there is a next drive
    if drive < amountOfDrives:
        # Check if next drive is empty
        if driveXHasCarrier[drive - 1 + 1] != 0:
            print("Carrier " + str(carrier) + " wants to go to drive " + str(drive + 1) + " ,but there is carrier " \
                  + str(driveXHasCarrier[drive - 1 + 1]) + " on there")
            evaluateDriveReset(drive + 1, driveXHasCarrier[drive - 1 + 1])

        driveXHasCarrier[drive - 1 + 1] = carrier

    # If the current drive is drive 1, then a new carrier is pulled onto the drive 1
    if drive == 1:
        print ("new carrier gets pulled")
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

    print ("After the carriers have moved ")
    print (driveXHasCarrier)
    # If the last carrier completed the run, run number +1


# If a carrier leaves the last drive, the data has to be compressed and the CSV file has to be saved
def completeRun(drive, carrier):
    compressData(drive, carrier)

    exportCSV(carrier)

    clearCarrierData(carrier)


# Compresses the data, so that only every X-th (KEEP_EVERY_X_ROW) is kept in the data
# Example: rows: 1,2,3,4,5,6 --> compressData with KEEP_EVERY_X_ROW == 2 --> rows: 1,3,5
def compressData(drive, carrier):
    print ("The drive ")
    print (drive)
    print ("reset its position")
    print (" ")
    logging.info("Compressing data of carrier: " + str(carrier))

    # the Value where the average is built
    valueAverage = 0
    # iterates through all the carrier data entries that have been made up to this point
    # the if else is just there to catch an out of bounds exception where the currentPosition is bigger than the array size of carrierData[2]
    # statement: do a if x < y else b ----> does a if x < y .. otherwise it does b
    print ("range: " + str(int(currentPositionAtCarrierData[carrier - 1])))

    for i in range(0, int(currentPositionAtCarrierData[carrier - 1])):

        #print ("i: " + str(i))
        # Saves the first x numbers to row 0, then the second x numbers to row 1 and so on
        saveTo = int(i / KEEP_EVERY_X_ROW)
        #print ("saveTo " + str(saveTo))

        # Time and position will just be overwritten so that it has 1,X,2X,3X,4X from KEEP_EVERY_X_ROW
        if int(i % KEEP_EVERY_X_ROW) == 0:
            carrierData[carrier - 1][0][saveTo] = carrierData[carrier - 1][0][i]
            carrierData[carrier - 1][1][saveTo] = carrierData[carrier - 1][1][i]
            carrierData[carrier - 1][2][saveTo] = carrierData[carrier - 1][2][i]
            carrierData[carrier - 1][3][saveTo] = carrierData[carrier - 1][2][i]
        else:
            # Test, so that the value at saveTo is not added to itself
            if saveTo != i:
                # Add the energy to calculate average
                carrierData[carrier - 1][3][saveTo] += carrierData[carrier - 1][2][i]

        #print (str(carrierData[carrier - 1][0][saveTo]) + "    " \
        #      + str(carrierData[carrier - 1][1][saveTo]) + "    " \
        #      + str(carrierData[carrier - 1][2][saveTo]) + "    " \
        #      + str(carrierData[carrier - 1][3][saveTo]))

        # if my current row is bigger than what the largest row to keep would be then empty that row
        if i >= 1 + int((currentPositionAtCarrierData[carrier - 1] - 1) / float(KEEP_EVERY_X_ROW)):
        #    print ("deleting row " + str(i))
            carrierData[carrier - 1][0][i] = 0
            carrierData[carrier - 1][1][i] = 0
            carrierData[carrier - 1][2][i] = 0
            carrierData[carrier - 1][3][i] = 0
        # If all the X amount lines are added up they then can be averaged
        # UPDATE: Instead of averaging, the sum is now kept

# Exports the table of the carrier to a CSV file in the form time; posAbsolute; posOnDrive; energy
def exportCSV(carrier):

    # print "Exporting: "
    # print carrierData[carrier - 1]

    # Creates the filename
    fileName = "Session_" + str(setConstants.SESSION) + "_Carrier_" + str(int(carrier)) + "_Iteration_" + str(int(runNumber)) + ".csv"

    # Adds the relative file path to the name that the files are saved to /InitialData/
    fileName = os.path.abspath(os.path.join("CarrierData", fileName))
    print ("filename " + str(fileName))

    firstRow = findFirstRowInCarrierData(carrier)
    print ("first Row " + str(firstRow))
    lastRow = int((currentPositionAtCarrierData[carrier - 1] - 1) / KEEP_EVERY_X_ROW)
    print ("last Row " + str(lastRow))

    export = np.transpose(carrierData[carrier - 1][:, firstRow:lastRow])

    # print "export"
    # print export

    np.savetxt(fileName, export, fmt='%0.5f', delimiter=DATA_SEPARATOR, newline='\n',
               header='time;posAbsolute;posOnDrive;energy', footer='', comments='# ')
    logging.info("Exported to file " + fileName)

# Finds the first row of the array that will be exported as CSV, where pos and energy consumption != 0
def findFirstRowInCarrierData(carrier):
    firstRow = 0
    for i in range(0, int(carrierData.shape[2]) - 1):
        if (carrierData[carrier - 1][1][i] == 0) and (carrierData[carrier - 1][2][i] == 0):
            firstRow = i
        else:
            return firstRow
    return firstRow


# Clear the data array for a certain carrier
def clearCarrierData(carrier):
    for i in range(0, int(carrierData.shape[2]) - 1):
        carrierData[carrier - 1][0][i] = 0
        carrierData[carrier - 1][1][i] = 0
        carrierData[carrier - 1][2][i] = 0
        carrierData[carrier - 1][3][i] = 0
    # Set the current position that is being filled to 0 so that the array can be filled again
    currentPositionAtCarrierData[carrier - 1] = 0


# Ensures enough space in the carrier data array for a certain carrier
def ensureEnoughSpaceInCarrierData(carrier):
    global carrierData
    if currentPositionAtCarrierData[carrier - 1] >= carrierData.shape[2]:
        carrierData = np.resize(carrierData,
                                (int(carrierData.shape[0]), int(carrierData.shape[1]), int(carrierData.shape[2] * 2)))


def modifyCSVFile(filename):

    # InputFileName und OutputFileName of CSV
    inputFileName = filename
    outputFileName = os.path.splitext(inputFileName)[0] + "_modified.csv"

    # Opens File
    with open(inputFileName, 'rb') as inFile, open(outputFileName, 'wb') as outfile:
        # defines reading file and writing file
        r = csv.reader(inFile, delimiter=setConstants.CSV_SEPARATOR)
        w = csv.writer(outfile, delimiter=setConstants.CSV_SEPARATOR)

        # Copys first row
        first_row = next(r)
        num_cols = len(first_row)

        # Initialize Array for new ColumnNames
        newColNames = []

        # Counter of Columns
        j = 0

        # Startposition of Positon Columns
        startPositonOfColumns = 0

        # Iterates the first row of the initial file and depending on the value writes columns into the file
        for i in first_row:
            # if j is zero
            if j == 0:
                newColNames.append("ms")
            # if column includes "iw4PowerCU" it's an energy sensor
            if "iw4PowerCU" in i:
                newColNames.append("energy" + str(j - 1))
            # if column includes "ExternalEncoderPosition" it's an position sensor
            if "ExternalEncoderPosition" in i:
                if startPositonOfColumns == 0:
                    startPositonOfColumns = j
                newColNames.append("position" + str(j - startPositonOfColumns))
                # counts the amount of drives.
                amountOfDrives = j - startPositonOfColumns

            j = j + 1

        # Skips the first row from the reader, the old header
        next(r, None)
        # Writes new header
        w.writerow(newColNames)

        # Copies the rest of reader
        for row in r:
            w.writerow(row)

        # Returns amountOfDrives
        return amountOfDrives

#########################################################
############# START OF SCRIPT ###########################
#########################################################

# Initialize Log-File
# Creates or loads Log DataProcessing.log
# Format of LogFile: mm/dd/yyyy hh:mm:ss PM LogMessage
logging.basicConfig(filename='dataProcessing.log',level=logging.INFO,format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')

# Creates a TextFile "Running.txt" on Start to let writeCarrierDataToDataBase.py know that the script is still running
with open("Running.txt", "w") as text_file:
    text_file.write("Running")
    logging.info("compressInitialData.py now running. 'Running.txt' created.")

# Write all DATA_FILE_NAMES in an Array
for files in glob.glob("InitialData/*.csv"):
    DATA_FILE_NAMES.append(files)
logging.info("Found " + str(len(DATA_FILE_NAMES)) + " new files.")

# Checks if a File is added to DATA_FILE_NAMES. If not it is terminating the script
if not DATA_FILE_NAMES:
    print ('No Files in Folder')
    # Removes Running.txt, so the simulator can also terminate
    os.remove("Running.txt")
    logging.info("Terminating compressInitialData.py. 'Running.txt' removed.")
    # Terminates the script
    sys.exit()

for fileName in DATA_FILE_NAMES:

    # Calls modifyCSVFile function
    amountOfDrives = modifyCSVFile (fileName)

    # Variables
    # Array that saves for every drive which carrier is on it
    driveXHasCarrier = np.zeros(amountOfDrives)
    # This is where all the data goes before exporting to CSV
    # carrierData[carrier number][time = 0, pos = 1, energy consumption = 2][position of array]
    carrierData = np.zeros((AMOUNT_OF_CARRIERS, 4, 100))
    # Here is stored in which row the last entry of carrier data was made for every carrier
    # (This could also be calculated by why not store it, since its used frequently)
    currentPositionAtCarrierData = np.zeros(AMOUNT_OF_CARRIERS)
    # Saves the last position on the drive of every carrier
    lastPositionOfCarrier = np.zeros(AMOUNT_OF_CARRIERS)
    # Number of complete runs through the system
    runNumber = 0
    # The amount of carriers who entered drive 1 (Therefore starting with carrier 1) in the current run
    carriersThroughTheSystem = 1

    # DATA_PATH creates an OS independent file path to the data files that were input as string names
    # Initialize empty DATA_PATH array
    DATA_PATH = ["" for x in range(DATA_FILE_NAMES.__sizeof__())]

    # Set first data path
    # This is needed when the data is in a subfolder
    # DATA_PATH[0] = os.path.abspath(os.path.join("data", DATA_FILE_NAMES[0]))
    DATA_PATH[0] = os.path.abspath(DATA_FILE_NAMES[0])

    # First row of data frames
    initialData = pd.read_csv(os.path.splitext(fileName)[0] + "_modified.csv", DATA_SEPARATOR, low_memory=False, header=0)
    #    Extracting the DriveNo of the first loaded File in DATA_PATH
    # Iterates each row and afterwards each drive
    #  Calls compressData with a pd.Series. The values are:
    # ms, No. of Drive, Energy Consmption, Position
    for index, row in initialData.iterrows():
        for drive in range(0, amountOfDrives):
            time = int(float(str(row['ms']).replace(',', '.')))
            position = float(str(row['position'+str(drive)]).replace(',', '.'))
            energy = float(str(row['energy' + str(drive)]).replace(',', '.'))
            processData([time, drive+1, position, energy])
        #sleep(WAIT_TIME_IN_SECONDS)

    # Moving data to
    # Moves the processed data files to InitialDataArchive
    # print "Moving processed files"
    # os.rename(fileName, os.path.abspath(os.path.join("InitialDataArchive", os.path.basename(fileName))))
    # print os.path.abspath(os.path.join("CarrierData", os.path.basename(fileName)))
    # logging.info("Moving " + fileName + " to: " + os.path.abspath(os.path.join("InitialDataArchive", os.path.basename(fileName))))

# Removes the status.txt file after the end of the simulation
os.remove("Running.txt")
logging.info("Terminating compressInitialData.py. 'Running.txt removed.")