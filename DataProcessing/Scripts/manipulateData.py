#!/usr/bin/env python

# This script processes all csv-files that are produced by dataProcessing.py on the fly.
# Therefor it reads out all csv-files and calculates all necessary measures before loading the data into the database.
# The input files have to follow the following convention:
# Naming: Session_X_Carrier_Y_Iteration_Z.csv (X, Y, Z = int of Session, Carrier & Iteration)
# CSV-Columns: 'timeStamp','positionAbsolute','positonOnDrive','energyConsumption'

# Imports libraries
# Imports os for Operating System independent absolute file paths
import os
# Imports sys to let the script die
import sys
# Imports glob to enable the script to search for all csv files in a particular folder
import glob
# Imports SQLAlchemy to Load pandas DataFrame to SQLITEDB
from sqlalchemy import create_engine
# Imports logging for logs
import logging
# Imports sleep for sleeping
from time import sleep
# Imports Pandas for Data handling
import pandas as pd
# Imports setConstants to import the Constants
import setConstants
import sqlite3


# Function that checks if new csv files are in the folder
def check_folder():
    for files in glob.glob("CarrierData/*.csv"):
        # Adds each file to the list dataFileNames
        dataFileNames.append(files)

    # Returns False or True depending on whether or not files are stored in dataFileNames
    if not dataFileNames:
        logging.info("No new files found")
        return False
    else:
        logging.info(str(len(dataFileNames)) + " Files found")
        return True


# Function to process each file
def process_file(fileName):
    logging.info("Processing " + fileName)
    # Loading Path of the file
    filePath = os.path.abspath(fileName)
    # Loading data into a dataFrame
    data = pd.read_csv(filePath, setConstants.CSV_SEPARATOR)
    # Change name of Columns to fit DataBaseModel
    data.columns = ['timeStamp', 'positionAbsolute', 'positionOnDrive', 'energyConsumption']
    # Reads out session of file name and adds column to DataFrame after Casting from str to int
    session = int(fileName.split('_')[1])
    data['session'] = session
    # Reads out carrier of file name and adds column to DataFrame after Casting from str to int
    carrier = int(fileName.split('_')[3])
    data['carrier'] = carrier
    # Reads out iteration of file name and aadds column to DataFrame after Casting from str to int
    iteration = int(fileName.split('_')[5].replace('.csv', ''))
    data['iteration'] = iteration
    # Calculates the speed between two datapoints (Way/Time)
    data['speed'] = data['positionAbsolute'].diff().divide(data['timeStamp'].diff())
    # Calculates acceleration (SpeedEnd * SpeedEnd - SpeedBeginn * SpeedBeginn))/distance * 2
    data['acceleration'] = data['speed'].multiply(data['speed']).diff().divide(
        data['positionAbsolute'].diff().multiply(2))

    # Rearanges the columns to fit them to the new database model
    # Reads out Columns to a list
    cols = data.columns.tolist()
    # Rearanges the columms
    cols = cols[4:7] + cols[0:1] + cols[2:3] + cols[1:2] + cols[7:9] + cols[3:4]
    # Reananges the dataframe data
    data = data[cols]

    # calls function to load the data into the database
    load_to_database(data, setConstants.NAME_TABLE_PROCESSED_DATA)

    # Creating DataFrame for the commulated Data
    # Calculating Measures
    # Calculates Average Energy Consumption
    averageEnergyConsumption = data['energyConsumption'].abs().mean()
    # Calculates Comulated Energy Consumption
    totalEnergyConsumption = data['energyConsumption'].sum()
    # Calculates Average Speed
    averageSpeed = data['speed'].mean()
    # Calculates Average Acceleration
    averageAcceleration = data['acceleration'].mean()

    # Inizialize DataFrame comulatedData with columns based on new DataBaseModel
    comaulatedData = pd.DataFrame(
        columns=['session', 'carrier', 'iteration', 'speedAverage', 'accelerationAverage',
                 'energyConsumptionTotal', 'energyConsumptionAverage'], index=['1'])
    # Adding previous extracted and calculated values to DataFrame
    comaulatedData.loc['1'] = pd.Series(
        {'session': session, 'carrier': carrier, 'iteration': iteration, 'speedAverage': averageSpeed,
         'accelerationAverage': averageAcceleration, 'energyConsumptionTotal': totalEnergyConsumption,
         'energyConsumptionAverage': averageEnergyConsumption})

    # calls function to load the processed data into the database
    load_to_database(comaulatedData, setConstants.NAME_TABLE_COM_DATA)

    # Move the processed data files to InitialDataArchive
    logging.info ("Moving processed files")
    #os.rename(fileName, os.path.abspath(os.path.join("CarrierDataArchive", os.path.basename(fileName))))
    logging.info("Moving file to archive: " + fileName)


# Loads data into the Database. Input = DataFrame
def load_to_database(data, tableName):
    logging.info("Loading DataFrame into Database...")

    data = data.fillna(0)

    logging.info("table name: " + tableName)

    # Creates SQL Alchemy Engine. Path to sqliteFile is enought. sqlite://// prefix is necessary
    # engine = create_engine('sqlite:////' + setConstants.PATH_OF_SQLLITE_DB)

    # Database connection
    con = sqlite3.connect(setConstants.PATH_OF_SQLLITE_DB)
    logging.info("Connection: " + con)

    # Query before
    df = pd.read_sql_query("SELECT * FROM " + tableName, con)
    print(df.head())

    # Loads dataframe to database. Appends data or creates table and is not adding the index of the dataFrame.
    data.to_sql(name = tableName, con = con, if_exists = 'append' ,index = False)
    print "pushed!"

    df = pd.read_sql_query("SELECT * FROM " + tableName, con)
    print(df.head())

    logging.info("Data loaded into Database")


#########################################################
############# START OF SCRIPT ###########################
#########################################################

# Initialize Log-File
# Creates or loads Log DataProcessing.log
# Format of LogFile: mm/dd/yyyy hh:mm:ss PM LogMessage
logging.basicConfig(filename='dataProcessing.log',level=logging.INFO,format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

# Putting Script a sleep for 0.5 sec to ensure that Running.txt is already created
logging.info("dataProcessing.py goes a sleep for 0.5 sec")
sleep(0.5)

# Initialize dataFileNames as list. (List has to be available for all functions thats why it's declared global
dataFileNames = []

# Check if Running.txt exist.
while os.path.isfile("Running.txt"):
    # Running.txt exists -> Check if there are already files distributed by dataProcessing.py
    logging.info("dataProcessing.py is still running")
    if check_folder():
        # If there are files which are not processed yet, call for each file process_file
        for filename in dataFileNames:
            process_file(str(filename))

    # put the script a sleep for setConstants.WAIT_TIME_IN_SECONDS_MPY before it checks the folder again for new files
    logging.info("manipulateData.py goes asleep for " + str(setConstants.WAIT_TIME_IN_SECONDS_MPY) + "Sec")
    sleep(setConstants.WAIT_TIME_IN_SECONDS_MPY)

else:

    # Running.txt does not exist. -> Check if the folder has files which hasn't been processed yet.
    logging.info("dataProcessing.py is not running")
    if check_folder():
        # If there are files which are not processed yet, call for each file process_file
        for filename in dataFileNames:
            process_file(filename)
    logging.info("manipulateData.py: Shut down")
