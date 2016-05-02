# @author AMOSus (Daniel)
# @author inkibus (Rene)

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
DATA_PATH = os.path.abspath(os.path.join("data", "daten_cleaning.csv"))
# DATA_SEPARATOR: Separator of the CSV-File
DATA_SEPARATOR = ';'
# The percentage that the data is compressed to (0.1 = 10%. This means that 10% of the data is kept)
COMPRESS_DATA_TO_PERCENT = 10

# Variables
linearDrivesData = np.zeros((AMOUNT_OF_DRIVES,3,100))
currentPositionAtDrive = np.zeros(AMOUNT_OF_DRIVES)
driveXHasCarrier = np.zeros(AMOUNT_OF_DRIVES)
carrierData = np.zeros((AMOUNT_OF_CARRIERS,3,100))
currentPositionAtCarrier = np.zeros(AMOUNT_OF_CARRIERS)
carrierAtPos = np.zeros(AMOUNT_OF_CARRIERS)
newRun = 1

def compressData(INPUT):
    print "Input"
    print INPUT
    print " "

    drive = int(INPUT[1])

    print "Drive"
    print drive
    print " "

    # Ensures that new Run is initialized before referencing
    global newRun

    #Ensures that carrier Data is called from global variables
    global carrierData
    # If the line has just started, then the first carrier enters the first drive
    # if driveXHasCarrier == np.zeros(AMOUNT_OF_CARRIERS): old version
    if newRun == 1:
        print "line has just started: Carrier 1 at Drive 1"
        print " "

        newRun = 0
        driveXHasCarrier[0] = 1


    carrier = int(driveXHasCarrier[drive-1])
    print "Carrier"
    print carrier
    print " "



    # If the current drive doesnt have a carrier, it cannot be mapped
    if driveXHasCarrier[drive-1] == 0:
        print "the Drive doesnt have a carrier, the data is deleted"
        #TODO maybe save the amount of data that is being deleted
        return

    # If the current Drive position has is 0 and was not 0 before, then the drive reset itself.
    # This means that now the data can be compressed, then the CSV file can be saved.
    # Also the current linearDrivesData should be cleared for that drive.
    if INPUT[3] == 0 & (INPUT[3] < carrierData[carrier-1][2][currentPositionAtCarrier[carrier-1]]):
        print "The drive "
        print drive
        print "reset its position"
        print " "

        #TODO reduce data size by deleting rows and calculating average values instead

        #TODO delete unncessary rows, where nothing changed

        #TODO export CSV file

        #TODO clear all Rows of that linear drive

        #TODO set current position to 0

    #Continue with processing the data

    #The data needs to be added to the array

    # Ensures enough space in the array
    if carrierData.shape[2] <= currentPositionAtCarrier[carrier]+1:

        carrierData = np.resize(carrierData, (int(carrierData.shape[0]),int(carrierData.shape[1]),int(carrierData.shape[2]*2)))


    # Transfer time in ms
    carrierData[carrier][0][currentPositionAtCarrier[carrier]] = INPUT[0]
    # Transfer position
    carrierData[carrier][1][currentPositionAtCarrier[carrier]] = INPUT[3]
    # Transfer energy consumption
    carrierData[carrier][2][currentPositionAtCarrier[carrier]] = INPUT[2]
    # So that next time the next row will be filled with data
    currentPositionAtCarrier[carrier] += 1

    return





# Loads Csv into a pandas DataFrame
InitialData = pd.read_csv(DATA_PATH, DATA_SEPARATOR)

a = InitialData.iterrows()

# Iterates each row and afterwards each drive
# Calls compressData with a pd.Series. The values are:
# ms, No. of Drive, Energy Consumption, Position
for index, row in InitialData.iterrows():
    for i in range(0, AMOUNT_OF_DRIVES):
        #TODO For me (RENE) just an array makes more sense than a Series here
        compressData(pd.Series([row['ms'], i + 1, row['energy' + str(i + 1)], row['pos' + str(i + 1)]]))
    sleep(WAIT_TIME_IN_SECONDS)
print carrierData
