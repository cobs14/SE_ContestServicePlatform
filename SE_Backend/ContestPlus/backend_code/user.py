from django.http import JsonResponse
from ContestPlus.backend_code.secure import *
from django.db.models import Q
import datetime
import threading
import os
import hashlib


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
                        'userType': u.userType, 'description': u.description, 'trueName': u.trueName}
        except User.DoesNotExist:
            return JsonResponse({'error': 'user not exist'})
        except SyntaxError:
            if us_type == 'error':
                return JsonResponse({'error': 'login'})
            response = {'id': user.id, 'username': user.username,
                        'major': user.major, 'email': user.email,
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
            if participation.checkStatus == 'reject':
                user_status['registered'] = 0
            elif participation.checkStatus == 'accept':
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
            if user_status['submitted'] and participation.grade == '':
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


def api_session(request):
    if request.method == 'POST':
        post = eval(request.body)
        try:
            username = post['username']
            password = post['password']
            user = User.objects.get(username=username)
            if not user.emailVerifyStatus:
                return JsonResponse({'error': 'need verify'})
            md5 = hashlib.md5()
            md5.update(post['password'].encode('utf-8'))
            if md5.hexdigest() == user.password:
                jwt_text = Jwt(user.email).encode()
                user.jwt = jwt_text
                user.save()
                return JsonResponse({'message': 'ok', 'id': user.id,
                                     'jwt': user.jwt, 'username': user.username,
                                     'userType': user.userType,
                                     'email': user.email, 'avatar': user.avatar})
            else:
                return JsonResponse({'error': 'wrong password'})
        except:
            user = User.objects.get(sessionId=post['session_id'])
        if user.userType == 'user':
            qr = qrcode.QRCode(version=5,
                               error_correction=qrcode.constants.ERROR_CORRECT_L,
                               box_size=10, border=4, )
            host_name = settings.host + '/apply/'
            try:
                email_code = EmailCode.objects.get(userId=user.id)
                email_code.code = random_str(8)
            except EmailCode.DoesNotExist:
                email_code = EmailCode(userId=user.id, userType='user', code=random_str(8))
            email_code.save()
            qr.add_data(host_name + email_code.code)
            qr.make(fit=True)
            qr_img = qr.make_image()
            qr_img = qr_img.resize((200, 200))
            image_dir = str(settings.BASE_DIR) + "/files/free/apply/"
            if not os.path.exists(image_dir):
                os.makedirs(image_dir)
            qr_img.save(image_dir + str(user.id) + '.png')
            return JsonResponse({'userType': 'user', 'session_id':
                                 user.sessionId, 'qrcode':
                settings.host +'/res/apply/' + str(user.id) + '.png'})
        elif user.userType == 'sponsor':
            response = {'userType': 'sponsor', 'session_id': user.sessionId, 'contestList': []}
            contest = Contest.objects.filter(sponsorId=user.id, censorStatus='accept', allowGroup=0)
            for i in contest:
                now_time = time.mktime(datetime.datetime.now().timetuple())
                if not now_time <= contest.contestDeadline:
                    continue
                response['contestList'].append({'id': i.id, 'title': i.title})
            return JsonResponse(response)
        else:
            return JsonResponse({'error': 'authority'})
    return JsonResponse({'error': 'need POST method'})


def api_offline(request):
    if request.method == 'POST':
        post = eval(request.body)
        try:
            sponsor = User.objects.get(sessionId=post['session_id'])
        except User.DoesNotExist:
            return JsonResponse({'error': 'session_id'})
        if sponsor.userType != 'sponsor':
            return JsonResponse({'error': 'authority'})
        try:
            contest = Contest.objects.get(id=post['contestId'])
            if contest.sponsorId != sponsor.id:
                return JsonResponse({'error': 'sponsorId'})
        except Contest.DoesNotExist:
            return JsonResponse({'error': 'contest'})
        try:
            email_code = EmailCode.objects.get(code=post['qrcode'])
            now_time = datetime.datetime.now()
            un_time = time.mktime(now_time.timetuple())
            un_time2 = time.mktime(email_code.sendTime.timetuple())
            if un_time2 + 3600 < un_time:
                return JsonResponse({'error': 'qrcode outdated'})
            user = User.objects.get(id=email_code.userId)
            try:
                _ = Participation.objects.get(targetContestId=contest.id, userId=user.id)
                return JsonResponse({'message': 'already applied', 'username':
                                     user.username, 'trueName': user.trueName})
            except Participation.DoesNotExist:
                participant = Participation(type='single', participantId=user.id,
                                            userId=user.id, targetContestId=contest.id,
                                            checkStatus='accept', completeStatus='completing')
                participant.save()
                return JsonResponse({'message': 'ok', 'username': user.username,
                                     'trueName': user.trueName})
        except EmailCode.DoesNotExist:
            return JsonResponse({'error': 'qrcode'})
    return JsonResponse({'error': 'need POST method'})
