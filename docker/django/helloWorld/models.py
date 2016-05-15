from django.db import models

# Database model
# Author: Inkibus (Rene R.)

class tbl_Session(models.Model):
    # It is not necessary to explicitly declare an ID

    # Every time something in the production system is changed, a new Session is stored, to have coherent data
    # Integer of the current session in which a carrier is in the system
    # This cannot be the primary key because the sessionNumber is dependent on the read CSV file
    sessionNumber = models.IntegerField()

class tbl_Carrier(models.Model):
    # It is not necessary to explicitly declare an ID

    # Integer that identifies the carrier
    # This cannot be the primary key because the carrierNumber is dependent on the read CSV file
    carrierNumber = models.IntegerField()

class tbl_Iteration(models.Model):
    # It is not necessary to explicitly declare an ID

    # Integer of the current Iteration in which a carrier is in the system
    # This number can get big so it is initialized as BigIntegerField
    # This cannot be the primary key because the iterationNumber is dependent on the read CSV file
    iterationNumber = models.BigIntegerField()

class tbl_TimeStampData(models.Model):
    # It is not necessary to explicitly declare an ID
    # Maybe necessary, because the implicit ID will not be a "BigInteger", which is required

    # The Session that the data is recorded for
    fid_Session = models.ForeignKey(tbl_Session, on_delete=models.CASCADE)
    # The Carrier that the data is recorded for
    fid_Carrier = models.ForeignKey(tbl_Carrier, on_delete=models.CASCADE)
    # The Iteration that the data is recorded for
    fid_Iteration = models.ForeignKey(tbl_Iteration, on_delete=models.CASCADE)

    # The time (in ms) from the beginning of the Iteration that the data is recorded
    timeStamp = models.BigIntegerField()
    # The position (relative to the beginning of the current drive, in mm) that the carrier is on
    positionOnDrive = models.FloatField()
    # The absolute position (relative to the beginning of the first drive, in mm) that the carrier is at
    positionAbsolute = models.FloatField()
    # The speed that the carrier has at that timeStamp (derived from the positionAbsolute and the timeStamps)
    speed = models.FloatField()
    # The acceleration that the carrier has at that timeStamp (derived from the positionAbsolute and the timeStamps)
    acceleration = models.FloatField()
    # The total amount of energy consumed by the carrier since the last timeStamp (in W)
    energyConsumption = models.FloatField()

class tbl_IterationData(models.Model):
    # It is not necessary to explicitly declare an ID
    # Maybe necessary, because the implicit ID will not be a "BigInteger", which is required

    # The Session that the data is recorded for
    fid_Session = models.ForeignKey(tbl_Session, on_delete=models.CASCADE)
    # The Carrier that the data is recorded for
    fid_Carrier = models.ForeignKey(tbl_Carrier, on_delete=models.CASCADE)
    # The Iteration that the data is recorded for
    fid_Iteration = models.ForeignKey(tbl_Iteration, on_delete=models.CASCADE)

    # The average speed of a carrier in one iteration
    speedAverage = models.FloatField()
    # The average acceleration of a carrier in one iteration
    accelerationAverage = models.FloatField()
    # The total energy Consumption of a carrier in one iteration
    energyConsumptionTotal = models.FloatField()
    # The average energy Consumption of a carrier in one iteration
    energyConsumptionAverage = models.FloatField()