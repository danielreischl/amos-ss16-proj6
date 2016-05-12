from django.db import models

class Carrier(models.Model):
    mass = models.FloatField()

class Time(models.Model):
    carrier = models.ForeignKey(Carrier, on_delete=models.CASCADE)
    timestamp = models.IntegerField()
    position = models.FloatField()

