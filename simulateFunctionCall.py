#@author AMOSus

#This script is a simple simulator of RealTimedata to enable the Algorythm to compress the Data in a proper way
#Input: CSV file with the following structure (ms, energy1, ..., energyX, pos1,...,posX) (x = Amount of Drives)
#The script calls depending on the amount of drives and waittime the CompressingAlgorythm all x seconds

#Imports Pandas for Datahandling and Sleep for waiting
import pandas as pd
from time import sleep

#Changeable Variables
#Waittime: Time the script should wait until it calls the function again (1 = 1 second - 0.001 = 1 millisecond)
#AmountOfDrives: How many Drives are producing data
#PathOfInitialData = Path of the CSV - File that should be simulated
#DataSeperator: Seperator of the CSV-File
waitTime = 0.001
amountOfDrives = 3
PathOfInitialData = 'data\daten_cleaning.csv'
DataSeperator = ';'

#DummyFunction that is called
def compressData (InputSeries):
    print InputSeries
    
#Loads Csv into a pandas DataFrame
InitialData = pd.read_csv(PathOfInitialData, DataSeperator)

#Iterates each row and afterwards each drive
#Calls compressData with a pd.Series. The values are:
#ms, No. of Drive, Energy Consumption, Position
for index,row in InitialData.iterrows():
    for i in range(0,amountOfDrives):
        compressData(pd.Series([row['ms'], i+1, row['energy' + str(i+1)], row['pos' + str(i+1)]]))
    sleep (waittime)
