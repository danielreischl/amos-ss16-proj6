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
import sys

sleep(0.5)

while os.path.isfile("Running.txt"):
    print "Simulator running"
    sleep(setConstants.WAIT_TIME_IN_SECONDS_MPY)

else:
    print "Simulator no longer running"
    sys.exit()



