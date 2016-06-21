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

from django.db import models

# Database model

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
    # The absolute time on which a carrier is on the drive
    timeAbsolute = models.IntegerField()

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


# Table in the databse that stores values for each session (Name Of the File, SessionNo, AmountOfCarriers, Status)
class sessiondata(models.Model):
    # Integer of session
    session = models.IntegerField()
    # Name of File
    fileName = models.TextField()
    # Integer of Amount Of Carriers in this session
    amountOfCarriers = models.IntegerField()
    # Status of Session (0 = Not Imported, 1 = Imported)
    status = models.BooleanField()

    def __unicode__(self):  # in python 3.3 this is __str__(self):
        return str(self.fid_Session)
