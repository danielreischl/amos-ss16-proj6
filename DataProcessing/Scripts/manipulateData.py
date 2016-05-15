# Imports Pandas for Data handling
import pandas as pd
# Imports OS for Operating System independent absolute file paths
import os
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
    data.columns = ['timeStamp','positionAbsolute','positonOnDrive','energyConsumption']
    # Reads out session of file name and add Column to DataFrame after Casting from str to int
    data['fidSession'] = int(fileName.split('_')[1])
    # Reads out carrier of file name and add Column to DataFrame after Casting from str to int
    data['fidCarrier'] = int(fileName.split('_')[3])
    # Reads out iteration of file name and add Column to DataFrame after Casting from str to int
    data['fidIteration'] = int(fileName.split('_')[5].replace('.csv',''))
    #calculates the speed between two datapoints (Way/Time)
    data['speed'] = data['positionAbsolute'].diff().divide(data['timeStamp'].diff())
    #Calculates acceleration (SpeedEnd * SpeedEnd - SpeedBeginn * SpeedBeginn))/distance * 2
    data['acceleration']= data['speed'].multiply(data['speed']).diff().divide(data['positionAbsolute'].diff().multiply(2))

    # Rearange the columns to fit them to the new database model
    # Reading out Columns to a list
    cols = data.columns.tolist()
    # Rearange the colums
    cols = cols[4:7] + cols[0:1] + cols[2:3] + cols [1:2] + cols[7:9] + cols[3:4]
    # Rearange the data frame
    data = data[cols]

    #calls function to load the data into the database
    load_to_database(data)

    #calls function to load and comulate the data into the database
    load_to_database_comulated(data)

    #TODO: moves the file to the Archive


#Loads data into the Database. Input = DataFrame
def load_to_database(data):

    print "Loading DataFrame into Database"

    #TODO: Load data to database


# Comaulates and loads the data into the database. Input =DataFrame
def load_to_database_comulated(data):
    # Calculates Average Energy Consumption
    averageEnergyConsumption = data['energyConsumption'].abs().mean()
    # Calculates Comulated Energy Consumption
    totalEnergyConsumption = data['energyConsumption'].sum()
    # Calculates Average Speed
    averageSpeed = data['speed'].mean()
    # Calculates Average Acceleration
    averageAcceleration = data['acceleration'].mean()
    # Reads out Session, Carrier and Iteration
    iteration = data['fidIteration'].mean()
    session = data ['fidSession'].mean()
    carrier = data ['fidCarrier'].mean()

    #Inizialize DataFrame comulatedData
    comulatedData = pd.DataFrame(columns=['fidSession','fidCarrier','fidIteration','averageSpeed', 'averageAcceleration', 'totalEnergyConsumption', 'averageEnergyConsumptionAbsolute'], index=['1'])
    #Adding Values to DataFrame
    comulatedData.loc['1'] = pd.Series ({'fidSession':session, 'fidCarrier': carrier, 'fidIteration':iteration, 'averageSpeed':averageSpeed, 'averageAcceleration':averageAcceleration, 'totalEnergyConsumption':totalEnergyConsumption, 'averageEnergyConsumptionAbsolute':averageEnergyConsumption})

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