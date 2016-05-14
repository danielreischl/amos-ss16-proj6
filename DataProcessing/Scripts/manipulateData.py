# Imports Pandas for Data handling
import pandas as pd
# Imports OS for Operating System independent absolute file paths
import os
# Imports Pandas for Data handling
import numpy as np
# Imports sleep for sleeping
from time import sleep
# Imports setConstants to import the Constants
import setConstants
# Imports glob to enable the script to search for all csv files in a particular folder
import glob
# Imports sys to let the script die
import sys

# Putting Script a sleep for 0.5 sec to ensure that Running.txt is already created
sleep(0.5)

#Function that checks if new csv files are in the folder
def check_folder():
    for files in glob.glob("CleanedDataFiles/*.csv"):
        DATA_FILE_NAMES.append(files)

    # Returns False or True depending on where file names are stored in the list or not
    if not DATA_FILE_NAMES:
        return False
    else:
        return True

# Function to process each file
def process_file(fileName):
    #Loading Path of the file
    filePath = os.path.abspath(fileName)
    Data = pd.read_csv(filePath, setConstants.CSV_SEPARATOR, index_col=0)

while os.path.isfile("Running.txt"):

    # Initalize List for Data file names
    DATA_FILE_NAMES = []
    if check_folder():
        for filename in DATA_FILE_NAMES:
            #calls the function process_file with each filename stored in DATA_FILE_NAMES
            process_file(filename)

    # Sleep Time before the script checks again if the file exists.
    sleep(setConstants.WAIT_TIME_IN_SECONDS_MPY)

    sys.exit()

else:
    # Needed to check if there are files in the folder which are not processed even after the simulator is no longer running
    print "Simulator no longer running"

    # Initalize List for Data file names
    DATA_FILE_NAMES = []
    if check_folder():
        for filename in DATA_FILE_NAMES:
            # calls the function process_file with each filename stored in DATA_FILE_NAMES
            process_file(filename)

    sys.exit()



