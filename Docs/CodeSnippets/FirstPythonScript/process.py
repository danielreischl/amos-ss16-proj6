# two libraries we might want to use - I recommend that we all use the abbreviations plt, np

from matplotlib import pyplot as plt
import numpy as np

# libraray for, well, processing csv

import csv

"""
@author: TobiDo
@test: Rene222

Not anything that I would expect to be in the project in the end,
just to play around with the data a bit and to let those who don't 
know python see what it looks like
"""


def csv2npArray(fileName):
    # function reads the csv-File <filename> 
    # and returns a numpy - Array with the file's content 
    file = open(fileName,'r')
    data_reader = csv.reader(file, delimiter = ';')
    
    # transform input 'stream' to matrix form
    # I found this somewhere on stackexchange and am a bit surprised that it also
    # works for more than one column
    data = [data for data in data_reader]
    
    # transform it to a numpy array
    npArray = np.asarray(data,dtype=float)
    return npArray
    

def getPosFromTime(time,array,start):
    """
    <array> is supposed to be a 2-dimensional array with time points in the 
    first row (array[:,0]) and position points in the second (array[:,1])

    the function returns position of carrier at time <time>
    if there is no exact entry, it returns position at smallest recorded 
    time after <time>

    example: for the following array 
    0 | 500
    2 | 550
    4 | 560
    6 | 565
    
    getPosFromTime(3,array,0) is 560
    getPosFromTime(4.5,array,0) is 565

    the function starts searching at line <start> of <array> 
    use this if you know that the time you are looking for is certainly stored after that line,
    otherwise use <start> = 0
    
    """
    for index in range(start,array.shape[0]):
        if (array[start,0] >= time):
            return array[start,1]
    
def getTimeFromPos(pos,array,start):
    """ 
    same as getTimeFromPos but with time and position switched
    """
    for index in range(start,array.shape[0]):
        if (array[index,1] >= pos):
            return (array[index,0],index)
    return (-1,-1)
    

def invertTimePos(timeToPos):
    """
    <array> is supposed to be a 2-dimensional array with time point in the 
    first row (array[:,0]) and position points in the second (array[:,1])
 
    the function returns an inverted array in the sense that the first row now
    contains _equidistant_ position points and the second row the first
    point of time when the carrier's position is bigger than the position in
    the first row
    
    this is useful if we want to know energy consumption at a certain position 
    but a priori only know energy consumption at given time
    """
    posToTime = np.zeros((1400,2)) #TODO: replace 1400 with maximal position
    newStart = 0
    for index in range(0,280,1): #TODO: replace 280 
        pos = index * 5 #5 is pretty arbitrary here -> change
        posToTime[index,0] = pos
        (newPos,newStart) = getTimeFromPos(pos,timeToPos,newStart)
        posToTime[index,1] = newPos
    return posToTime


position = csv2npArray('./data-examples/pos.csv')
energy = csv2npArray('./data-examples/energy.csv')


# now add speed in a third column

speed = np.zeros((position.shape[0],3))
for i in range(position.shape[0]-2000):
    #just copy entries for time and position
    speed[i,0] = position[i,0]
    speed[i,1] = position[i,1]
    if i > 0:
        # do a simple computation of speed: how much did it move in the last time period
        # denominator is 1 in example file
        # probably we should take some average here
        speed[i,2] = (position[i,1] - position[i-1,1])/(position[i,0] - position[i-1,0])

plt.plot(speed[:,0],speed[:,1])
plt.show()

plt.plot(speed[:,0],speed[:,2])
plt.show()



posToTime = invertTimePos(position)
plt.plot(posToTime[:,0],posToTime[:,1])
plt.show()

plt.plot(energy[:,0],energy[:,1])
plt.plot(energy[:,0],energy[:,2])
plt.show()
