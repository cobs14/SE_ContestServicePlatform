from django.db import models


class User(models.Model):
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=256)
    email = models.EmailField(max_length=64)
    emailVerifyStatus = models.BooleanField(default=False)
    userType = models.CharField(max_length=16, default='user')  # user用户，sponsor举办方，admin管理员
    loginStatus = models.BooleanField(default=False)

    pubKey = models.CharField(max_length=512, blank=True)
    priKey = models.CharField(max_length=512, blank=True)
    jwt = models.CharField(max_length=512, blank=True)

    avatar = models.CharField(max_length=128,blank=True)

    qualificationStatus = models.CharField(max_length=16, default='guest')  # guest游客，qualified验证后的用户
    OutdateTime = models.DateTimeField(blank=True,null=True,editable=True)
    documentNumberNeeded = models.BooleanField(default=True, blank=True)
    documentNumber = models.CharField(max_length=32, blank=True)
    trueName = models.CharField(max_length=32, blank=True)
    birthTime = models.DateField(null=True, blank=True)


class EmailCode(models.Model):
    userType = models.CharField(max_length=16)
    userId = models.CharField(max_length=16)
    code = models.CharField(max_length=8)
    sendTime = models.DateTimeField(auto_now=True)


class Contest(models.Model):
    title = models.CharField(max_length=256)
    abstract = models.CharField(max_length=512, blank=True)
    description = models.TextField(blank=True)

    module = models.CharField(max_length=256)
    link = models.CharField(max_length=256, blank=True,null=True) # 官网
    thumb = models.CharField(max_length=218,blank=True,null=True)

    sponsorId = models.IntegerField(default=0)
    allowGroup = models.BooleanField(default=False)
    maxGroupMember = models.IntegerField(default=1)
    minGroupMember = models.IntegerField(default=1)
    censorStatus = models.CharField(max_length=16, default='pending') # pending审核中，accept通过，reject拒绝

    applyStartTime = models.DateTimeField()
    applyDeadline = models.DateTimeField()
    contestStartTime = models.DateTimeField()
    contestDeadline = models.DateTimeField()
    reviewStartTime = models.DateTimeField()
    reviewDeadline = models.DateTimeField()


class Participation(models.Model):
    type = models.CharField(default='single', max_length=16) # single单人，group多人
    participantId = models.IntegerField(default=0)
    targetContestId = models.IntegerField(default=0)
    checkStatus = models.CharField(max_length=16, default='pending') # pending审核中，accept通过，reject拒绝
    completeStatus = models.CharField(max_length=16, default='ready') # ready准备中，competing竞赛中，completed完成
    grade = models.IntegerField(default=0)
    fullGrade = models.IntegerField(default=100)
    awardTitle = models.CharField(max_length=256, blank=True)
    awardContent = models.TextField(blank=True)


class Group(models.Model):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=256)
    memberCount = models.IntegerField()
    memberId = models.CharField(max_length=256) # 形如 '1,3,6'


class Counter(models.Model):
    name = models.CharField(max_length=64)
    value = models.IntegerField(default=0)


class Picture(models.Model):
    picture_id = models.IntegerField()
    url = models.CharField(max_length=128)
    hostType = models.CharField(max_length=16,default='none')
    hostId = models.IntegerField()