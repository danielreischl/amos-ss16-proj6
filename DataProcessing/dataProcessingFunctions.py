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

# Imports os
import os
# Imports logging
import logging
# Imports glob
import glob
# Import Configparser
import ConfigParser
# Imports Sys
import sys
# Imports SqLite
import sqlite3
# Imports ConfigParser
import ConfigParser

# Creates a TextFile "Running.txt" on Start to let writeCarrierDataToDataBase.py know that the script is still running
def createRunningFile():
    with open("/srv/DataProcessing/Running.txt", "w") as text_file:
        text_file.write("Running")
        logging.info("compressInitialData.py now running. 'Running.txt' created.")


# Removes the status.txt file after the end of the simulation and writes its status to log file
def deleteRunningFile():
    os.remove("/srv/DataProcessing/Running.txt")
    logging.info("Terminating compressInitialData.py. 'Running.txt removed.")

# Checks for .csv Files in particular folder and returns a list
def checkForCSVFilesInFolder(folder):
    dataFileNames = []
    for files in glob.glob(folder+"/*.csv"):
        dataFileNames.append(files)
    logging.info("Found " + str(len(dataFileNames)) + " new files.")
    return dataFileNames

# Function that checks if new csv files are in the folder
def check_folder(dataFileNames):

    # Returns False or True depending on whether or not files are stored in dataFileNames
    if not dataFileNames:
        logging.info("No new files found")
        return False
    else:
        logging.info(str(len(dataFileNames)) + " Files found")
        return True

# Updates the Config File
# Input: Section of ConfigFile, sectionValue, value
def updated_config(section, sectionValue, value):
    # Reads ConfigFile from the absolute Filepath
    config = ConfigParser.ConfigParser()
    config.read('/srv/DataProcessing/settings.cfg')

    # Sets the value of a particular section, sectionValue combination
    config.set(section, sectionValue, value)

    # Wirtes the new ConfigFile with the absolute FilePath
    with open('/srv/DataProcessing/settings.cfg', 'wb') as configfile:
        config.write(configfile)

# Writes a Pandas DataFrame to the Database
# Input PandasDataFrame, TableName, ifExist
def write_dataframe_to_database (data, tableName, ifExist):
    # Reads ConfigFile
    config = ConfigParser.ConfigParser()
    config.read('settings.cfg')

    logging.info("Loading DataFrame into Database...")

    data = data.fillna(0)

    logging.info("table name: " + tableName)

    # Connects Script to DataBase
    try:
        # Opens connection to DataBsae
        con = sqlite3.connect(config.get('Paths', 'database'))
        # Adds "DataBase Connection: Success" after successfully connecting to database
        logging.info("DataBase Connection: Success")
    except:
        # Adds Error to Log if connection to DataBase failed
        logging.error("DataBase Connection: Fail")
        # Adds database Path to ease the debugging
        logging.error("DataBase Path: " + config.get('Paths', 'database'))
        # Terminates the script with 0 and prints the message
        sys.exit("DataBase Connection Failed")

    # Loads dataframe to database. Appends data or creates table and is not adding the index of the dataFrame.
    data.to_sql(name=tableName, con=con, if_exists=ifExist, index=False)
    print "pushed!"

    logging.info("Data loaded into Database")


