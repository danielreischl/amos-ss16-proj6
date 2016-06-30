#!/usr/bin/env python

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

# This script processes all csv-files that are produced by compressInitialData.py on the fly.
# Therefor it reads out all csv-files and calculates all necessary measures before loading the data into the database.
# The input files have to follow the following convention:
# Naming: Session_X_Carrier_Y_Iteration_Z.csv (X, Y, Z = int of Session, Carrier & Iteration)
# CSV-Columns: 'timeStamp','positionAbsolute','positonOnDrive','energyConsumption'

# Imports libraries
# Imports os for Operating System independent absolute file paths
import os
# Imports sys to let the script die
import sys
# Imports logging for logs
import logging
# Imports sleep for sleeping
from time import sleep
# Imports Pandas for Data handling
import pandas as pd
# Imports dataProcessingFunctions.py
import dataProcessingFunctions
# Imports ConfigParser
import ConfigParser

# Function to process each file
def process_file(fileName):
    logging.info("Processing " + fileName)
    # Loading Path of the file
    filePath = os.path.abspath(fileName)
    # Loading data into a dataFrame
    data = pd.read_csv(filePath, config.get('Simulation','csv_seperator'))
    # Change name of Columns to fit DataBaseModel
    data.columns = ['timeStamp', 'positionAbsolute', 'energyConsumption', 'drive','timeAbsolute']
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
    data['speed'] = data['positionAbsolute'].diff().div(data['timeStamp'].diff())
    # Calculates acceleration (Speed2 - Speed1)/ (time2 - time1)
    data['acceleration'] = data['speed'].diff().div(data['timeStamp'].diff())

    # Rearanges the columns to fit them to the new database model
    # Reads out Columns to a list
    cols = data.columns.tolist()
    # Rearanges the columms
    cols = cols[5:8] + cols[0:1] + cols[3:4] + cols[1:2] + cols[8:10]  + cols[2:3] + cols[4:5]
    # Reananges the dataframe data
    data = data[cols]

    # calls function to load the data into the database
    dataProcessingFunctions.write_dataframe_to_database(data, config.get('database_tables','continuous'),'append')

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
    # Energy Consumption peak
    energyConsumptionPeak = data['energyConsumption'].max()
    # Spikepercentage
    energyConsumptionPercent = round((energyConsumptionPeak/averageEnergyConsumption)*100,2)

    # Inizialize DataFrame comulatedData with columns based on new DataBaseModel
    cumulatedData = pd.DataFrame(
        columns=['session', 'carrier', 'iteration', 'speedAverage', 'accelerationAverage',
                 'energyConsumptionTotal', 'energyConsumptionAverage', 'energyConsumptionPeak', 'energyConsumptionPercent'], index=['1'])
    # Adding previous extracted and calculated values to DataFrame
    cumulatedData.loc['1'] = pd.Series(
        {'session': session, 'carrier': carrier, 'iteration': iteration, 'speedAverage': averageSpeed,
         'accelerationAverage': averageAcceleration, 'energyConsumptionTotal': totalEnergyConsumption,
         'energyConsumptionAverage': averageEnergyConsumption,'energyConsumptionPeak': energyConsumptionPeak,
         'energyConsumptionPercent': energyConsumptionPercent})

    # calls function to load the processed data into the database
    dataProcessingFunctions.write_dataframe_to_database(cumulatedData, config.get('database_tables','average'),'append')

def moveFileToFolder(fileName, folderName):
    print ("Moving: " + fileName + " to " + os.path.join(folderName, os.path.basename(fileName)))
    logging.info("Moving: " + fileName + " to " + os.path.join(folderName, os.path.basename(fileName)))
    os.rename(fileName, os.path.abspath(os.path.join(folderName, os.path.basename(fileName))))

#########################################################
############# START OF SCRIPT ###########################
#########################################################

# Initialize Log-File
# Creates or loads Log DataProcessing.log
# Format of LogFile: mm/dd/yyyy hh:mm:ss PM LogMessage
logging.basicConfig(filename='/srv/DataProcessing/dataProcessing.log',level=logging.INFO,format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

# Reads ConfigFile
config = ConfigParser.ConfigParser()
config.read('settings.cfg')


# Putting Script a sleep the defined amount of time in the config file
logging.info("writeCarrierDataToDatabase.py goes a sleep for % sec" % config.getfloat('Simulation','waittime_first_dataload'))
sleep(config.getfloat('Simulation','waittime_first_dataload'))

# Initialize dataFileNames as list. (List has to be available for all functions thats why it's declared global
dataFileNames = []

# Check if Running.txt exist.
while os.path.isfile("Running.txt"):
    # Calls function dataProcessingFunctions.checkForCSVFilesInFolder to get back all csv Files saved in CarrierData
    dataFileNames = dataProcessingFunctions.checkForCSVFilesInFolder("CarrierData")

    # Running.txt exists -> Check if there are already files distributed by compressInitialData.py
    logging.info("compressInitialData.py is still running")
    if dataProcessingFunctions.check_folder(dataFileNames):
        # If there are files which are not processed yet, call for each file process_file
        for fileName in dataFileNames:
            process_file(str(fileName))

            # Move the processed data files to CarrierDataArchive
            moveFileToFolder(str(fileName), "CarrierDataArchive")

        # Clears dataFileNames
        dataFileNames = []

    # put the script a sleep for in config defined time before it checks the folder again for new files
    logging.info("writeCarrierDataToDatabase.py goes a sleep for % sec" % config.getfloat('Simulation', 'waittime_data_reload'))
    sleep(config.getfloat('Simulation', 'waittime_data_reload'))

else:
    # Calls function dataProcessingFunctions.checkForCSVFilesInFolder to get back all csv Files saved in CarrierData
    dataFileNames = dataProcessingFunctions.checkForCSVFilesInFolder("CarrierData")

    # Running.txt does not exist. -> Check if the folder has files which hasn't been processed yet.
    logging.info("compressInitialData.py is not running")
    if dataProcessingFunctions.check_folder(dataFileNames):
        # If there are files which are not processed yet, call for each file process_file
        for fileName in dataFileNames:
            process_file(fileName)

            # Move the processed data files to CarrierDataArchive
            moveFileToFolder(str(fileName), "CarrierDataArchive")

        # Clears dataFileNames
        dataFileNames = []
    logging.info("writeCarrierDataToDataBase.py: Shut down")
