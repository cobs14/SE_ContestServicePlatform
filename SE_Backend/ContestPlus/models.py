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


class Sponsor(models.Model):
    sponsorName = models.CharField(max_length=64)
    password = models.CharField(max_length=256)
    email = models.EmailField(max_length=64)
    emailVerifyStatus = models.BooleanField(default=False)
    loginStatus = models.BooleanField()
    checkStatus = models.CharField(max_length=64)


class EmailCode(models.Model):
    userType = models.CharField(max_length=16)
    userId = models.CharField(max_length=16)
    code = models.CharField(max_length=8)
    sendTime = models.DateTimeField(auto_now=True)

class Contest(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    module = models.CharField(max_length=256)
    sponserId = models.IntegerField()
    allowGroup = models.BooleanField()
    maxGroupMember = models.IntegerField()
    minGroupMember = models.IntegerField()
    censorStatus = models.BooleanField()

    applyStartTime = models.DateTimeField()
    applyDeadline = models.DateTimeField()
    contestStartTime = models.DateTimeField()
    contestDeadline = models.DateTimeField()
    reviewStartTime = models.DateTimeField()
    reviewDeadline = models.DateTimeField()
