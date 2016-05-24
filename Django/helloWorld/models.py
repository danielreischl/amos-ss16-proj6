#   This file is part of rogueVision.
#
#   Copyright (C) 2016 Daniel Reischl, Rene Rathmann, Peter Tan,
#       Tobias Dorsch, Shefali Shukla, Vignesh Govindarajulu,
#       Aleksander Penew, Abinav Puri
#
#   ReqTracker is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   ReqTracker is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PUROSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with rogueVision.  If not, see <http://www.gnu.org/licenses/>.

from django.db import models

# Database model
# Author: inkibus (Rene R.)

''' Commented out as this tables doesn't serve any purpose other than storing its primary key
class session(models.Model):
    # Every time something in the production system is changed, a new Session is stored, to have coherent data
    # Integer of the current session in which a carrier is in the system
    # This cannot be the primary key because the sessionNumber is dependent on the read CSV file
    sessionNumber = models.IntegerField(primary_key=True, unique=True, default=0)

    # Display the session number of this database entry
    def __unicode__(self): # in python 3.3 this is __str__(self):
        return "Session " + str(self.sessionNumber)


class carrier(models.Model):
    # Integer that identifies the carrier
    # This cannot be the primary key because the carrierNumber is dependent on the read CSV file
    carrierNumber = models.IntegerField(primary_key=True, unique=True, default=0)

    # Display the session number of this database entry
    def __unicode__(self):  # in python 3.3 this is __str__(self):
        return "Carrier " + str(self.carrierNumber)

class iteration(models.Model):
    # Integer of the current Iteration in which a carrier is in the system
    # This number can get big so it is initialized as BigIntegerField
    # This cannot be the primary key because the iterationNumber is dependent on the read CSV file
    iterationNumber = models.BigIntegerField(primary_key=True, unique=True, default=0)

    # Display the session number of this database entry
    def __unicode__(self):  # in python 3.3 this is __str__(self):
        return "Iteration " + str(self.iterationNumber)
'''

# This table stores all the relevant data for every data point recorded by the sensors
class timestampdata(models.Model):
    # It is not necessary to explicitly declare a primary key when using django models

    ''' Commented out as these tables don't serve any purpose other than storing their keys
    # The Session that the data is recorded for
    #fid_Session = models.ForeignKey(session, on_delete=models.CASCADE)
    # The Carrier that the data is recorded for
    #fid_Carrier = models.ForeignKey(carrier, on_delete=models.CASCADE)
    # The Iteration that the data is recorded for
    #fid_Iteration = models.ForeignKey(iteration, on_delete=models.CASCADE)
    '''

    # Integer of the current session in which a carrier is in the system
    session = models.IntegerField()
    # Integer that identifies the carrier
    carrier = models.IntegerField()
    # Integer of the current Iteration in which a carrier is in the system
    iteration = models.IntegerField()


    # The time (in ms) from the beginning of the Iteration that the data is recorded
    timeStamp = models.BigIntegerField()
    # The drive that the carrier was on when this timeStamp was recorded
    drive = models.IntegerField()
    # The absolute position (relative to the beginning of the first drive, in mm) that the carrier is at
    positionAbsolute = models.FloatField()
    # The speed that the carrier has at that timeStamp (derived from the positionAbsolute and the timeStamps)
    speed = models.FloatField()
    # The acceleration that the carrier has at that timeStamp (derived from the positionAbsolute and the timeStamps)
    acceleration = models.FloatField()
    # The total amount of energy consumed by the carrier since the last timeStamp (in W)
    energyConsumption = models.FloatField()

    # Display the session, carrier and iteration and time stamp number of this database entry
    def __unicode__(self):  # in python 3.3 this is __str__(self):
        return "S_" + str(self.fid_Session) + "_C_" + str(self.fid_Carrier) + "_I_" + str(self.fid_Iteration) \
               + "_T_" + str(self.timeStamp)

# This table stores all the data that is calculated over the course of one iteration (sums and averages)
class iterationdata(models.Model):
    # It is not necessary to explicitly declare a primary key when using django models

    ''' Commented out as these tables don't serve any purpose other than storing their keys
    # The Session that the data is recorded for
    #fid_Session = models.ForeignKey(session, on_delete=models.CASCADE)
    # The Carrier that the data is recorded for
    #fid_Carrier = models.ForeignKey(carrier, on_delete=models.CASCADE)
    # The Iteration that the data is recorded for
    #fid_Iteration = models.ForeignKey(iteration, on_delete=models.CASCADE)
    '''

    # Integer of the current session in which a carrier is in the system
    session = models.IntegerField()
    # Integer that identifies the carrier
    carrier = models.IntegerField()
    # Integer of the current Iteration in which a carrier is in the system
    iteration = models.IntegerField()


    # The average speed of a carrier in one iteration
    speedAverage = models.FloatField()
    # The average acceleration of a carrier in one iteration
    accelerationAverage = models.FloatField()
    # The total energy Consumption of a carrier in one iteration
    energyConsumptionTotal = models.FloatField()
    # The average energy Consumption of a carrier in one iteration
    energyConsumptionAverage = models.FloatField()

    # Display the session, carrier and iteration number of this database entry
    def __unicode__(self):  # in python 3.3 this is __str__(self):
        return "S_" + str(self.fid_Session) + "_C_" + str(self.fid_Carrier) + "_I_" + str(self.fid_Iteration)