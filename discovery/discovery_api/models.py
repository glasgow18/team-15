# Create your models here.
from django.db import models


# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Activity(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


class Warnings(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


class ContactDetail(models.Model):
    name = models.CharField(max_length=25)
    email = models.CharField(max_length=30, null=True, blank=True)
    url = models.CharField(max_length=100, null=True, blank=True)
    contactNumber1 = models.IntegerField(null=True, blank=True)
    contactNumber2 = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name


class KeyWord(models.Model):
    tag = models.CharField(max_length=20)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.tag


class Location(models.Model):
    name = models.CharField(max_length=100)
    free = models.BooleanField(default=True)
    price = models.IntegerField()
    description = models.CharField(max_length=1000)
    address = models.CharField(max_length=100, null=True)
    contact = models.ForeignKey(ContactDetail, on_delete=models.SET_NULL, null=True, blank=True)
    possibleActivities = models.CharField(max_length=1000)

    keyWords = models.ManyToManyField(KeyWord, help_text="tags")
    warnings = models.ManyToManyField(Warnings, help_text="warnings")
    activities = models.ManyToManyField(Activity, help_text="tags")

    lat = models.FloatField(null=True, blank=True)
    long = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    userName = models.CharField(max_length=20)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    reviewDescription = models.CharField(max_length=1000)
