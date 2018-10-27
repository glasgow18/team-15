from django.db import models


# Create your models here.
class Location(models.Model):
    name = models.CharField(max_length=100)
    free = models.BooleanField(default=True)
    price = models.IntegerField()
    description = models.CharField(max_length=1000)
