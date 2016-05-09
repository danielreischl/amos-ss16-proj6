import numpy as np
import math
from matplotlib import pyplot as plt


# a script to create dummy data -- preliminary version
# TODO: documentation, restructuring, csv export, bugfixes   

lineLength = 10000
driveLength = 5000
T1 = 50
T2 = 50

# the function describe position/velocity/acceleration of 
# carriers RELATIVE to their entry point

def positionFunction(time):
    if time < T1:
        return (1 - np.cos(time * np.pi / (2*T1))) * driveLength
    else:
        return (time-T1)*(np.pi/(2*T1)) * driveLength + driveLength
        

def velocityFunction(time):
    if time < T1:
        return (np.sin(time * np.pi / (2*T1))) * np.pi / (2*T1) * driveLength
    else:
        return (np.pi/(2*T1)) * driveLength

def accelerationFunction(time):
    if time < T1:
        return np.cos(time * np.pi /(2*T1)) / (4*T1*T1) * np.pi * np.pi * driveLength
    else:
        return 0

def energyFunction(time):
        mass = 1
        return mass*velocityFunction(time)*accelerationFunction(time)
    


class Carrier:
    entryTime = -1 # time when carriers enters line

    def __init__(self, entryTime,endTime):
        self.entryTime = entryTime  # TODO make this a global variable
        self.endTime = endTime        
    def getPosition(self,time):
        # get position of this carrier with respect to the global time frame
        if time < self.entryTime:
            # carrier is not yet on the line
            return -1
        else:
            return positionFunction(time - self.entryTime)
    def getEnergy(self, time):
        # get energy of this carrier with respect to the global time frame
        if time < self.entryTime:
            return 0
        else:
            return energyFunction(time - self.entryTime)

class Drive:
    # variables data store position and energy data
    endTime = 0 # TODO: make global   
    drivePosition = 0 #position where the drive 'begins'
    def __init__(self, drivePosition, endTime) :
        self.drivePosition = drivePosition
        self.endTime = endTime
        self.data = np.zeros((endTime+1,3))
        for time in range(endTime):
            self.data[time,0] = time
            
    def addPositionPoint(self,time,position,energy):
        self.data[time,1] = position-self.drivePosition
        self.data[time,2] = energy
        
    def export2Csv():
        return
        

class Data:
    numberOfCarriers = 0
    numberOfDrives = 0
    driveLength = 0
    endTime = 0
    carriers = []
    drives = []


    def __init__(self,entryTimes,numberOfDrives,driveLength, endTime):
        self.driveLength = driveLength
        self.numberOfDrives = numberOfDrives
        self.endTime = endTime
        self.numberOfCarriers = len(entryTimes)
        
        for entryTime in entryTimes:
                self.carriers.append(Carrier(entryTime, endTime))

        for driveNumber in range(numberOfDrives):
            self.drives.append(Drive(driveNumber*driveLength,endTime))


        
    def getDrive(self,position):
        # returns the drive to which the position belongs
        driveNumber = int(position/self.driveLength)
        if driveNumber >= self.numberOfDrives or position < 0:
            return None
        else:
            return self.drives[driveNumber]
            
    def createDummy(self):
            for time in range(self.endTime+1):
                    for carrier in self.carriers:
                        # for each carrier get the drive that it is on
                        position = carrier.getPosition(time)
                        drive = self.getDrive(position)
                        if drive is not None:
                            drive.addPositionPoint(time,position, carrier.getEnergy(time))
    

d = Data([1,60,],2,5000,100)

d.createDummy()
drive1 = d.drives[0]
drive2 = d.drives[1]
 #drive*.data contains position and energy information