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
import logging
# Imports glob
import glob


# Creates a TextFile "Running.txt" on Start to let writeCarrierDataToDataBase.py know that the script is still running
def createRunningFile():
    with open("Running.txt", "w") as text_file:
        text_file.write("Running")
        logging.info("compressInitialData.py now running. 'Running.txt' created.")


# Removes the status.txt file after the end of the simulation and writes its status to log file
def deleteRunningFile():
    os.remove("Running.txt")
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