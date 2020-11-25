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
    type = models.CharField(max_length=32)
    password = models.CharField(max_length=256)
    email = models.EmailField(max_length=64)
    emailVerifyStatus = models.BooleanField(default=False)
    loginStatus = models.BooleanField(default=False)
    checkStatus = models.CharField(max_length=64)
    pubKey = models.CharField(max_length=512, blank=True)
    priKey = models.CharField(max_length=512, blank=True)
    jwt = models.CharField(max_length=512, blank=True)


class EmailCode(models.Model):
    userType = models.CharField(max_length=16)
    userId = models.CharField(max_length=16)
    code = models.CharField(max_length=8)
    sendTime = models.DateTimeField(auto_now=True)


class Contest(models.Model):
    title = models.CharField(max_length=256)
    abstract = models.CharField(max_length=512,blank=True)
    description = models.TextField()
    module = models.CharField(max_length=256)

    sponsorId = models.IntegerField(default=0)
    allowGroup = models.BooleanField(default=False)
    maxGroupMember = models.IntegerField(default=1)
    minGroupMember = models.IntegerField(default=1)
    censorStatus = models.BooleanField(default=False)

    applyStartTime = models.DateTimeField()
    applyDeadline = models.DateTimeField()
    contestStartTime = models.DateTimeField()
    contestDeadline = models.DateTimeField()
    reviewStartTime = models.DateTimeField()
    reviewDeadline = models.DateTimeField()


class Participation(models.Model):
    type = models.CharField(default='single',max_length=16)
    participantId = models.IntegerField(default=0)
    targetContestId = models.IntegerField(default=0)
    checkStatus = models.BooleanField(default=False)
    completeStatus = models.BooleanField(default=False)
    grade = models.IntegerField(default=0)
    fullGrade = models.IntegerField(default=100)
    awardTitle = models.CharField(max_length=256)
    awardContent = models.TextField()
