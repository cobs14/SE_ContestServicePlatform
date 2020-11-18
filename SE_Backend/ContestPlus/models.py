from django.db import models


class User(models.Model):
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=256)
    email = models.EmailField(max_length=64)
    emailVerifyStatus = models.BooleanField(default=False)
    loginStatus = models.BooleanField(default=False)
    qualificationStatus = models.CharField(max_length=16)
    documentNumberNeeded = models.BooleanField(default=False)
    documentNumber = models.CharField(max_length=32)
    trueName = models.CharField(max_length=32)
    birthTime = models.DateField(null=True, blank=True)
    pubKey = models.CharField(max_length=512, blank=True)
    priKey = models.CharField(max_length=512, blank=True)
    jwt = models.CharField(max_length=512, blank=True)


class Sponsor(models.Model):
    sponsorName = models.CharField(max_length=64)
    password = models.CharField(max_length=256)
    email = models.EmailField(max_length=64)
    emailVerifyStatus = models.BooleanField(default=False)
    loginStatus = models.BooleanField()
    checkStatus = models.CharField(max_length=64)
    pubKey = models.CharField(max_length=512, blank=True)
    priKey = models.CharField(max_length=512, blank=True)
    jwt = models.CharField(max_length=512, blank=True)


class EmailCode(models.Model):
    userType = models.CharField(max_length=16)
    userId = models.IntegerField()
    code = models.CharField(max_length=8)
    sendTime = models.DateTimeField(auto_now=True)



