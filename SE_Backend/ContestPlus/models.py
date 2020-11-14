from django.db import models


class User(models.Model):
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=256)
    email = models.EmailField(max_length=64)
    loginStatus = models.BooleanField()
    qualificationStatus = models.CharField(max_length=16)
    documentNumberNeeded = models.BooleanField()
    documentNumber = models.BooleanField()
    trueName = models.CharField(max_length=32)
    birthTime = models.DateField()


class Sponsor(models.Model):
    sponsorName = models.CharField(max_length=64)
    password = models.CharField(max_length=256)
    email = models.EmailField(max_length=64)
    loginStatus = models.BooleanField()
    checkStatus = models.CharField(max_length=64)


class EmailCode(models.Model):
    userType = models.CharField(max_length=16)
    userId = models.IntegerField(max_length=16)
    code = models.CharField(max_length=6)
    sendTime = models.DateField()



