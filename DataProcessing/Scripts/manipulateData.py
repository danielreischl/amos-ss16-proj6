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
    for files in glob.glob("CarrierData/*.csv"):
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
    #Loading data into a dataFrame
    data = pd.read_csv(filePath, setConstants.CSV_SEPARATOR)
    #Change name of Columns

    #TODO: positionDrive will be added as soon as the data is in the input
    #TODO: Rename all Columns to the final names
    data.columns = ['ms','positionABS','energy']
    # Reads out session of file name and add Column to DataFrame
    data['session'] = fileName.split('_')[1]
    # Reads out carrier of file name and add Column to DataFrame
    data['carrier'] = fileName.split('_')[3]
    # Reads out iteration of file name and add Column to DataFrame
    data['iteration'] = fileName.split('_')[5].replace('.csv','')
    #calculates the speed between two datapoints (Way/Time)
    data['speed'] = data['positionABS'].diff().divide(data['ms'].diff())
    #Calculates acceleration (SpeedEnd * SpeedEnd - SpeedBeginn * SpeedBeginn))/distance * 2
    data['acceleration']= data['speed'].multiply(data['speed']).diff().divide(data['positionABS'].diff().multiply(2))

    #calls function to load the data into the database
    load_to_database(data)

    #calls function to load and comulate the data into the database
    load_to_database_comulated(data)

    #TODO: moves the file to the Archive


#Loads data into the Database. Input = DataFrame
def load_to_database(data):

    print "Loading DataFrame into Database"

    #TODO: Load data to database
    #data.to_sql()

# Comaulates and loads the data into the database. Input =DataFrame
def load_to_database_comulated(data):
    # Calculates Average Energy Consumption
    averageEnergyConsumption = data['energy'].mean()
    # Calculates Comulated Energy Consumption
    comulatedEnergyConsumption = data['energy'].sum()
    # Calculates Average Speed
    averageSpeed = data['speed'].mean()
    # Calculates Average Acceleration
    averageAcceleration = data['acceleration'].mean()

    #Inizialize DataFrame comulatedData
    comulatedData = pd.DataFrame(columns=['averageSpeed', 'averageEnergy', 'comEnergy', 'averageAcceleration'], index=['1'])
    #Adding Values to DataFrame
    comulatedData.loc['1'] = pd.Series ({'averageSpeed':1, 'averageEnergy':averageEnergyConsumption, 'comEnergy':comulatedEnergyConsumption, 'averageAcceleration':averageAcceleration})

    # TODO: Load data to database
    #comulatedData.to_sql()
    print "Loading comulated Dataframe to Database"

while os.path.isfile("Running.txt"):

    # Initalize List for Data file names
    DATA_FILE_NAMES = []
    if check_folder():
        for filename in DATA_FILE_NAMES:
            #calls the function process_file with each filename stored in DATA_FILE_NAMES and casts it into a string
            process_file(str(filename))

    # Sleep Time before the script checks again if the file exists.
    sleep(setConstants.WAIT_TIME_IN_SECONDS_MPY)

    # Terminates script for test purposes
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