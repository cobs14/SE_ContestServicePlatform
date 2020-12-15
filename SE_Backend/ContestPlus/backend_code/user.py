from django.http import JsonResponse
from ContestPlus.backend_code.secure import *
from django.db.models import Q
import datetime
import os


def api_user_contact(request):
    if request.method == 'POST':
        us_type, user = user_type(request)
        if us_type == 'error':
            return JsonResponse({'error': 'login'})
        try:
            post = eval(request.body)
            page_num = post['pageNum']
            page_size = post['pageSize']
        except (SyntaxError, KeyError):
            return JsonResponse({"error": "invalid parameters"})
        retrieved_dialog = Dialog.objects.filter(receiver=user.id)\
                                 .order_by('-updateTime')
        if page_num <= 0 or page_size <= 0:
            start_pos = 0
            end_pos = len(retrieved_dialog)
        else:
            start_pos = (page_num - 1) * page_size
            end_pos = page_num * page_size
        response = {'contact': retrieved_dialog[start_pos: end_pos]}
        return JsonResponse(response)
    return JsonResponse({'error': 'need POST method'})


def api_user(request):
    if request.method == 'POST':
        us_type, user = user_type(request)
        try:
            post = eval(request.body)
            u = User.objects.get(id=post['id'])
            response = {'id': u.id, 'username': u.username, 'avatar': u.avatar,
                        'email': u.email, 'major': u.major, 'school': u.school,
                        'userType': u.userType, 'description': u.description}
        except User.DoesNotExist:
            return JsonResponse({'error': 'user not exist'})
        except SyntaxError:
            if us_type == 'error':
                return JsonResponse({'error': 'login'})
            response = {'id': user.id, 'username': user.username,
                        'major': user.major, 'email': user.email,
                        'documentNumber': user.documentNumber,
                        'avatar': user.avatar, 'userType': user.userType,
                        'school': user.school, 'groupCode': user.groupCode,
                        'studentNumber': user.studentNumber,
                        'address': user.address, 'mobile': user.mobile,
                        'description': user.description,
                        'trueName': user.trueName}
        return JsonResponse(response)
    return JsonResponse({'error': 'need POST method'})


def api_user_retrieve(request):
    if request.method == 'POST':
        us_type, user = user_type(request)
        try:
            post = eval(request.body)
            params = post['params']
            page_num = post['pageNum']
            page_size = post['pageSize']
        except (SyntaxError, KeyError):
            return JsonResponse({"error": "invalid parameters"})
        try:
            if params['userType'] != '' and params['userType'] != 'any':
                retrieved_user = User.objects\
                                     .filter(emailVerifyStatus=1,
                                             userType=params['userType'])
            else:
                retrieved_user = User.objects.filter(emailVerifyStatus=1)
        except KeyError:
            retrieved_user = User.objects.filter(emailVerifyStatus=1)

        get_me = params['getMe']
        if get_me == 0 and us_type != 'error':
            retrieved_user = retrieved_user.filter(~Q(id=user.id))
        username = params['username']
        if len(username) > 0:
            retrieved_user = retrieved_user.filter(username__contains=username)
        school = params['school']
        if len(school) > 0:
            retrieved_user = retrieved_user.filter(school__contains=school)
        major = params['major']
        if len(major) > 0:
            retrieved_user = retrieved_user.filter(major__contains=major)
        student_number = params['studentNumber']
        if len(student_number) > 0:
            retrieved_user = retrieved_user\
                .filter(studentNumber__contains=student_number)

        if page_num <= 0 or page_size <= 0:
            start_pos = 0
            end_pos = len(retrieved_user)
        else:
            start_pos = (page_num - 1) * page_size
            end_pos = page_num * page_size
        response = {'count': retrieved_user.count()}
        response_user = []
        for z in retrieved_user[start_pos: end_pos]:
            response_user_ele = {'id': z.id, 'username': z.username,
                                 'avatar': z.avatar, 'school': z.school,
                                 'major': z.major, 'userType': z.userType}
            response_user.append(response_user_ele)
        response['data'] = response_user
        return JsonResponse(response)
    return JsonResponse({'error': 'need POST method'})


def api_user_check_relation(request):
    if request.method == 'POST':
        post = eval(request.body)
        us_type, user = user_type(request)
        if us_type == 'error':
            return JsonResponse({'error': 'login'})
        if us_type != 'user':
            return JsonResponse({'isUser': 0})
        try:
            contest = Contest.objects.get(id=post['contestId'])
        except Contest.DoesNotExist:
            return JsonResponse({'error': 'contest not exist'})
        response = {'isUser': 1}
        user_status = {'registered': 0}
        try:
            participation = Participation.objects\
                                         .get(targetContestId=contest.id,
                                              userId=user.id)
            user_status['registered'] = 1
            user_status['verified'] = 0
            user_status['submitted'] = 0
            if participation.checkStatus == 'accept':
                user_status['verified'] = 1
            if user_status['verified'] and contest.allowGroup:
                group = Group.objects.get(id=participation.participantId)
                user_group = {'groupName': group.name, 'data': [],
                              'description': group.description}
                s = group.memberId.split(',')
                for j in s:
                    user = User.objects.get(id=int(j))
                    user_group['data'].append({'id': user.id,
                                               'email': user.email,
                                               'username': user.username,
                                               'school': user.school,
                                               'major': user.major,
                                               'avatar': user.avatar})
                response['userGroup'] = user_group
            if participation.completeStatus == 'completed':
                user_status['submitted'] = 1
            if user_status['submitted']:
                try:
                    user_submission = {'filename': participation.submissionName,
                                       'fileSize': os.path.getsize(
                                           participation.submissionDir)}
                    response['userSubmission'] = user_submission
                except OSError:
                    user_status['submitted'] = 0
                    participation.completeStatus = 'completing'
                    participation.save()
        except Participation.DoesNotExist:
            pass
        response['userStatus'] = user_status
        return JsonResponse(response)
    return JsonResponse({'error': 'need POST method'})


def api_user_group_code(request):
    if request.method == 'POST':
        us_type, user = user_type(request)
        if us_type == 'error':
            return JsonResponse({'error': 'login'})
        if us_type != 'user':
            return JsonResponse({'error': 'authority'})
        now_time = time.mktime(datetime.datetime.now().timetuple())
        if user.groupCodeGenerateTime + 60 >= now_time:
            return JsonResponse({'error': 'too frequent'})
        user.groupCodeGenerateTime = now_time
        user.save()
        return JsonResponse({'newGroupCode': update_group_code(user.id)})
    return JsonResponse({'error': 'need POST method'})


def api_user_info(request):
    if request.method == 'POST':
        post = eval(request.body)
        us_type, user = user_type(request)
        if us_type == 'error':
            return JsonResponse({'error': 'login'})
        try:
            mobile = post['mobile']
            user.mobile = mobile
        except KeyError:
            pass
        try:
            address = post['address']
            user.address = address
        except KeyError:
            pass
        try:
            description = post['description']
            user.description = description
        except KeyError:
            pass
        user.save()
        return JsonResponse({'message': 'ok'})
    return JsonResponse({'error': 'need POST method'})
