import random
import time
import datetime
import rsa
import hashlib
import requests
from django.http import JsonResponse
from django.conf import settings
from django.core.mail import send_mail
from ContestPlus.backend_code.models import *
from ContestPlus.backend_code.secure import *


def apiContestStatus(request):

    if request.method == 'POST':
        post = eval(request.body)
        utype, _ = user_type(request)
        if utype != 'admin':
            return JsonResponse({'error': 'login'})
        try:
            contest = Contest.objects.get(id=post['id'])
            if contest.censorStatus != 'Pending':
                return JsonResponse({'error': 'status'})
        except:
            return JsonResponse({'error': 'contest'})
        if post['status']:
            contest.censorStatus = 'Accept'
        else:
            contest.censorStatus = 'Reject'
        contest.save()
        return JsonResponse({'message': 'ok'})
    return JsonResponse({'error': 'need POST method'})


def apiContestApply(request, contestId):
    if request.method == 'POST':
        post = eval(request.body)
        utype, user = user_type(request)
        if utype != 'user':
            return JsonResponse({'error': 'login'})
        try:
            contest = Contest.objects.get(id=contestId)
            if contest.censorStatus != 'Accept':
                return JsonResponse({'error': 'status'})
            now_time = time.mktime(datetime.datetime.now().timetuple())
            un_time = time.mktime(contest.applyStartTime.timetuple())
            un_time2 = time.mktime(contest.applyDeadline.timetuple())
            if not (un_time <= now_time <= un_time2):
                return JsonResponse({'error': 'applyTime'})
        except Contest.DoesNotExist:
            return JsonResponse({'error': 'contest'})
        if not contest.allowGroup:
            participation = Participation(participantId=user.id,
                                          targetContestId=contestId)
        else:
            member = str(post['participantId'][0])
            for i in post['participantId'][1:]:
                member += ',' + str(i)
            group = Group(name=post['groupName'],
                          description=post['description'],
                          memberCount=len(post['participantId']),
                          memberId=member)
            group.save()
            participation = Participation(participantId=group.id,
                                          targetContestId=contestId)
        participation.save()
        return JsonResponse({'message': 'ok'})
    return JsonResponse({'error': 'need POST method'})


def apiContestCreation(request):
    if request.method == 'POST':
        post = eval(request.body)
        utype, user = user_type(request)
        if utype == 'error':
            return JsonResponse({'error': 'login'})
        if utype != 'sponsor':
            return JsonResponse({'error': 'authority'})
        contest = Contest(title=post['title'], module=post['module'],
                          description=post['description'],
                          allowGroup=post['allowGroup'], sponsorId=user.id,
                          applyStartTime=post['applyStartTime'],
                          applyDeadline=post['applyDeadline'],
                          contestStartTime=post['contestStartTime'],
                          contestDeadline=post['contestDeadline'],
                          censorStatus=False, abstract=post['abstract'],
                          reviewStartTime=post['reviewStartTime'],
                          reviewDeadline=post['reviewDeadline'])
        if post['allowGroup']:
            contest.maxGroupMember = post['maxGroupMember']
            contest.minGroupMember = post['minGroupMember']
        contest.save()
        return JsonResponse({'message': 'ok', 'id': contest.id})
    return JsonResponse({'error': 'need POST method'})


def apiContestModify(request):
    if request.method == 'POST':
        post = eval(request.body)
        contest_id = post['contestId']
        modify_attribute = post['modifyAttribute']
        modify_value = post['modifyValue']

        utype, user = user_type(request)
        if utype == 'error':
            return JsonResponse({'error': 'login'})
        if utype != 'sponsor':
            return JsonResponse({'error': 'authority'})
        contest = Contest.objects.filter(id=contest_id)
        if len(contest) > 0:
            target_contest=contest[0]
            if modify_attribute == 'title':
                target_contest.title = modify_value
            elif modify_attribute == 'module':
                target_contest.module = modify_value
            elif modify_attribute == 'abstract':
                target_contest.abstract = modify_value
            elif modify_attribute == 'description':
                target_contest.description = modify_value
            elif modify_attribute == 'allowGroup':
                target_contest.allowGroup = modify_value
            elif modify_attribute == 'applyStartTime':
                target_contest.applyStartTime = modify_value
            elif modify_attribute == 'applyDeadline':
                target_contest.applyDeadline = modify_value
            elif modify_attribute == 'contestStartTime':
                target_contest.contestStartTime = modify_value
            elif modify_attribute == 'contestDeadline':
                target_contest.contestDeadline = modify_value
            elif modify_attribute == 'reviewStartTime':
                target_contest.reviewStartTime = modify_value
            elif modify_attribute == 'reviewDeadline':
                target_contest.reviewDeadline = modify_value
            elif modify_attribute == 'minGroupMember':
                target_contest.minGroupMember = modify_value
            elif modify_attribute == 'maxGroupMember':
                target_contest.maxGroupMember = modify_value
            else:
                return JsonResponse({'error': 'attribute invalid'})
            target_contest.save()
        else:
            return JsonResponse({'error': 'contest not found'})
        return JsonResponse({'message': 'ok', 'id': contest.id})
    return JsonResponse({'error': 'need POST method'})
