import random
import time
import datetime
import rsa
from Crypto.Cipher import AES
import base64
import hashlib
import jwt
import requests
from django.http import JsonResponse
from django.conf import settings
from django.core.mail import send_mail
from .models import *

false = False
true = True


class Aes:
    def __init__(self, key):
        self.key = key
        self.mode = AES.MODE_CBC

    def decrypt(self, text):
        cryptor = AES.new(self.key, self.mode, self.key)
        plain_text = cryptor.decrypt(base64.decodebytes(text.encode())).decode()
        return plain_text.rstrip('\0')


class Jwt:
    headers = {
        "alg": "HS256",
        "typ": "JWT"
    }
    salt = "asdfghjkl"

    def __init__(self, name):
        self.payload = {
            'name': name,
            'exp': int(time.time() + 86400)
        }

    def encode(self):
        token = jwt.encode(payload=self.payload, key=Jwt.salt, algorithm='HS256',
                           headers=Jwt.headers).decode('utf-8')
        return token


def apiRegister(request):
    if request.method == 'POST':
        try:
            request_body = eval(request.body)
            username = request_body.get('username')
            password = request_body.get('password')
            email = request_body.get('email')
        except:
            return JsonResponse({"error": "invalid parameters"})
        # 处理重复情况
        new_user = User(username=username, password=password, email=email)
        user = User.objects.filter(username=username)
        if len(user) > 0:
            for z in user:
                if z.emailVerifyStatus:
                    return JsonResponse({"error": "username exists"})
                else:
                    new_user = z  # 已有未验证用户
                    break
        user = User.objects.filter(email=email)
        if len(user) > 0:
            for z in user:
                if z.emailVerifyStatus:
                    return JsonResponse({"error": "email exists"})
                else:
                    new_user = z  # 已有未验证用户
                    break
        new_user.username = username
        new_user.password = password
        new_user.email = email
        new_user.save()

        # 发送邮件
        code = random_str()
        email_code = EmailCode.objects.filter(userId=new_user.id)
        if len(email_code) > 0:
            new_email_code = email_code[0]
            now_time = datetime.datetime.now()
            un_time = time.mktime(now_time.timetuple())
            un_time2 = time.mktime(new_email_code.sendTime.timetuple())
            if un_time2 + 60 > un_time:
                return JsonResponse({"error": "email still valid"})
            new_email_code.code = code
            new_email_code.save()
        else:
            new_email_code = EmailCode(userId=new_user.id, userType='user', code=code)
            new_email_code.save()
        send_message = "Your verification link is \n" + 'http://127.0.0.1:8080/register/verification/' + code  # 本机调试版
        send_mail("Contest Plus Email Verification", send_message, settings.DEFAULT_FROM_EMAIL, [email])
        return JsonResponse({"message": "ok"})
    return JsonResponse({'error': 'need POST method'})


def random_str():
    _str = '1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    return ''.join(random.choice(_str) for i in range(8))


def user_type(request):
    try:
        user = User.objects.get(jwt=request.META.get('HTTP_JWT'))
    except User.DoesNotExist:
        return 'error', None
    return user.userType, user


def apiContestRetrieve(request):
    if request.method == 'POST':
        try:
            request_body = eval(request.body)
            params = request_body.get('params')
            pageNum = request_body.get('pageNum')
            pageSize = request_body.get('pageSize')
        except:
            return JsonResponse({"error": "invalid parameters"})
        retrieved_contest = Contest.objects.all()

        contest_id = params['id']
        if contest_id != 0:
            retrieved_contest = retrieved_contest.filter(id=contest_id)
        sponsor_id = params['sponsorId']
        if sponsor_id != 0:
            retrieved_contest = retrieved_contest.filter(sponsorId=sponsor_id)

        allow_group = params['allowGroup']
        if allow_group != "Any":
            if allow_group == 'True':
                retrieved_contest = retrieved_contest.filter(allowGroup=True)
            if allow_group == 'False':
                retrieved_contest = retrieved_contest.filter(allowGroup=False)

        censorStatus = params['censorStatus']
        if censorStatus != "Any":
            if censorStatus == 'Pending':
                usertype, _ = user_type(request)
                if usertype != 'admin':
                    return JsonResponse({'error': 'authority'})
                retrieved_contest = retrieved_contest.filter(censorStatus='pending')
            if censorStatus == 'Accept':
                retrieved_contest = retrieved_contest.filter(censorStatus='accept')
            if censorStatus == 'Reject':
                usertype, _ = user_type(request)
                if usertype != 'admin':
                    return JsonResponse({'error': 'authority'})
                retrieved_contest = retrieved_contest.filter(censorStatus='reject')

        module = params['module']
        if len(module) > 0:
            module_retrieved_contest = Contest.objects.none()
            for z in module:
                module_retrieved_step = retrieved_contest.filter(module__contains=z)
                module_retrieved_contest = module_retrieved_contest | module_retrieved_step
            retrieved_contest = module_retrieved_contest

        text = params['text']
        if len(text) > 0:
            title_text_retrieved_contest = Contest.objects.none()
            for z in text:
                title_text_retrieved_step = retrieved_contest.filter(title__contains=z)
                title_text_retrieved_contest = title_text_retrieved_contest.union(title_text_retrieved_step)

            abstract_text_retrieved_contest = Contest.objects.none()
            for z in text:
                abstract_text_retrieved_step = retrieved_contest.filter(abstract__contains=z)
                abstract_text_retrieved_contest = abstract_text_retrieved_contest.union(abstract_text_retrieved_step)

            description_text_retrieved_contest = Contest.objects.none()
            for z in text:
                description_text_retrieved_step = retrieved_contest.filter(description__contains=z)
                description_text_retrieved_contest = description_text_retrieved_contest.union \
                    (description_text_retrieved_step)
            retrieved_contest = title_text_retrieved_contest.union \
                (abstract_text_retrieved_contest, description_text_retrieved_contest)

        state = params['state']
        apply = state['apply']
        contest = state['contest']
        review = state['review']

        if apply != 0:
            if apply == 1:
                now_time = datetime.datetime.now()
                un_time_now = time.mktime(now_time.timetuple())
                beforeApply = Contest.objects.none()
                for z in retrieved_contest:
                    un_time_apply_start = time.mktime(z.applyStartTime.timetuple())
                    if un_time_now < un_time_apply_start:
                        beforeApply = beforeApply.union(Contest.objects.filter(id=z.id))
                retrieved_contest = beforeApply

            if apply == 2:
                now_time = datetime.datetime.now()
                un_time_now = time.mktime(now_time.timetuple())
                duringApply = Contest.objects.none()
                for z in retrieved_contest:
                    un_time_apply_start = time.mktime(z.applyStartTime.timetuple())
                    un_time_apply_end = time.mktime(z.applyDeadline.timetuple())
                    if un_time_apply_end > un_time_now > un_time_apply_start:
                        duringApply = duringApply.union(Contest.objects.filter(id=z.id))
                retrieved_contest = duringApply

            if apply == 3:
                now_time = datetime.datetime.now()
                afterApply = Contest.objects.none()
                for z in retrieved_contest:
                    un_time_now = time.mktime(now_time.timetuple())
                    un_time_apply_end = time.mktime(z.applyDeadline.timetuple())
                    if un_time_apply_end < un_time_now:
                        afterApply = afterApply.union(Contest.objects.filter(id=z.id))
                retrieved_contest = afterApply

        if contest != 0:
            if contest == 1:
                now_time = datetime.datetime.now()
                un_time_now = time.mktime(now_time.timetuple())
                beforeContest = Contest.objects.none()
                for z in retrieved_contest:
                    un_time_contest_start = time.mktime(z.contestStartTime.timetuple())
                    if un_time_now < un_time_contest_start:
                        beforeContest = beforeContest.union(Contest.objects.filter(id=z.id))
                retrieved_contest = beforeContest

            if contest == 2:
                now_time = datetime.datetime.now()
                un_time_now = time.mktime(now_time.timetuple())
                duringContest = Contest.objects.none()
                for z in retrieved_contest:
                    un_time_contest_start = time.mktime(z.contestStartTime.timetuple())
                    un_time_contest_end = time.mktime(z.contestDeadline.timetuple())
                    if un_time_contest_end > un_time_now > un_time_contest_start:
                        duringContest = duringContest.union(Contest.objects.filter(id=z.id))
                retrieved_contest = duringContest

            if contest == 3:
                now_time = datetime.datetime.now()
                un_time_now = time.mktime(now_time.timetuple())
                afterContest = Contest.objects.none()
                for z in retrieved_contest:
                    un_time_contest_end = time.mktime(z.contestDeadline.timetuple())
                    if un_time_now > un_time_contest_end:
                        afterContest = afterContest.union(Contest.objects.filter(id=z.id))
                retrieved_contest = afterContest

        if review != 0:
            if review == 1:
                now_time = datetime.datetime.now()
                un_time_now = time.mktime(now_time.timetuple())
                beforeReview = Contest.objects.none()
                for z in retrieved_contest:
                    un_time_review_start = time.mktime(z.reviewStartTime.timetuple())
                    if un_time_now < un_time_review_start:
                        beforeReview = beforeReview.union(Contest.objects.filter(id=z.id))
                retrieved_contest = beforeReview
            if review == 2:
                now_time = datetime.datetime.now()
                un_time_now = time.mktime(now_time.timetuple())
                duringReview = Contest.objects.none()
                for z in retrieved_contest:
                    un_time_review_start = time.mktime(z.applyStartTime.timetuple())
                    un_time_review_end = time.mktime(z.reviewDeadline.timetuple())
                    if un_time_review_end > un_time_now > un_time_review_start:
                        duringReview = duringReview.union(Contest.objects.filter(id=z.id))
                retrieved_contest = duringReview
            if review == 3:
                now_time = datetime.datetime.now()
                un_time_now = time.mktime(now_time.timetuple())
                afterReview = Contest.objects.none()
                for z in retrieved_contest:
                    un_time_review_end = time.mktime(z.reviewDeadline.timetuple())
                    if un_time_now > un_time_review_end:
                        afterReview = afterReview.union(Contest.objects.filter(id=z.id))
                retrieved_contest = afterReview

        if pageNum == 0 or pageSize == 0:
            start_pos = 0
            end_pos = len(retrieved_contest)
        else:
            start_pos = (pageNum - 1) * pageSize
            end_pos = pageNum * pageSize
        response = {}
        response['count'] = retrieved_contest.count()
        response_contest = []
        for z in retrieved_contest[start_pos:end_pos]:
            response_contest_ele = {}
            response_contest_ele['id'] = z.id
            response_contest_ele['title'] = z.title
            sponsor = User.objects.filter(id=z.sponsorId)
            if len(sponsor) > 0:
                response_contest_ele['sponsor'] = sponsor[0].username
            else:
                response_contest_ele['sponsor'] = ''
            response_contest_ele['abstract'] = z.abstract
            response_contest_ele['module'] = z.module
            state = {}
            state['apply'] = [z.applyStartTime, z.applyDeadline]
            state['contest'] = [z.contestStartTime, z.contestDeadline]
            state['review'] = [z.reviewStartTime, z.reviewDeadline]
            response_contest_ele['state'] = state
            response_contest_ele['allowGroup'] = z.allowGroup
            # response_contest_ele['imgUrl'] = z.imgUrl
            response_contest_ele['imgUrl'] = "None"
            #
            detailed = params['detailed']
            if detailed == True:
                response_contest_ele['description'] = z.description
            response_contest.append(response_contest_ele)

        response['data'] = response_contest
        return JsonResponse(response)
    return JsonResponse({'error': 'need POST method'})


def apiRegisterVerifyMail(request):
    if request.method == 'POST':
        post = eval(request.body)
        if post.get('code'):
            try:
                response = JsonResponse({'message': 'ok'})
                email_code = EmailCode.objects.get(code=post['code'])
                now_time = datetime.datetime.now()
                un_time = time.mktime(now_time.timetuple())
                un_time2 = time.mktime(email_code.sendTime.timetuple())
                if un_time2 + 3600 < un_time:
                    response = JsonResponse({'error': 'code outdated'})
                else:
                    pub_key, pri_key = rsa.newkeys(512)
                    user = None
                    if email_code.userType == 'user':
                        user = User.objects.get(id=email_code.userId)
                    else:
                        user = User.objects.get(id=email_code.userId)
                    user.emailVerifyStatus = True
                    user.pubKey = pub_key.save_pkcs1().decode()
                    user.priKey = pri_key.save_pkcs1().decode()
                    user.save()
                email_code.delete()
                return response
            except EmailCode.DoesNotExist:
                return JsonResponse({'error': 'no such a code'})
        else:
            return JsonResponse({'error': 'blank request'})
    return JsonResponse({'error': 'need POST method'})


def apiKey(request):
    if request.method == 'POST':
        post = eval(request.body)
        user = None
        if post.get('username'):
            try:
                user = User.objects.get(username=post['username'])
            except User.DoesNotExist:
                return JsonResponse({'error': 'no such a user'})
        elif post.get('email'):
            try:
                user = User.objects.get(username=post['email'])
            except User.DoesNotExist:
                return JsonResponse({'error': 'no such a user'})
        if user:
            if user.emailVerifyStatus:
                return JsonResponse({'message': 'ok', 'key': user.pubKey})
            else:
                return JsonResponse({'error': 'need verification'})
        return JsonResponse({'error': 'blank request'})
    return JsonResponse({'error': 'need POST method'})


def apiLogin(request):
    if request.method == 'POST':
        post = eval(request.body)
        user = None
        if post.get('username'):
            user = User.objects.get(username=post['username'])
        elif post.get('email'):
            user = User.objects.get(username=post['email'])
        # pri_key = rsa.PrivateKey.load_pkcs1(user.priKey.encode())
        # key = rsa.decrypt(post['key'].encode(), pri_key)
        # aes = Aes(key)
        # password = aes.decrypt(post['password'])
        md5 = hashlib.md5()
        md5.update(post['password'].encode('utf-8'))
        if md5.hexdigest() == user.password:
            jwt_text = Jwt(user.email).encode()
            user.jwt = jwt_text
            user.save()
            return JsonResponse({'message': 'ok', 'id': user.id,
                                 'jwt': user.jwt, 'username': user.username,
                                 'email': user.email})
        else:
            return JsonResponse({'error': 'wrong password'})
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


def apiQualification(request):
    if request.method == 'POST':
        usertype, _ = user_type(request)
        if usertype == 'error':
            return JsonResponse({'error': 'login'})
        if usertype != 'user':
            return JsonResponse({'error': 'authority'})
        try:
            request_body = eval(request.body)
            username = request_body.get('username')
            xuexincode = request_body.get('xuexincode')
            documentNumber = request_body.get('documentNumber')
        except:
            return JsonResponse({"error": "invalid parameters"})
        headers = {"Connection": "close"}
        url = "https://www.chsi.com.cn/xlcx/bg.do?vcode=" + xuexincode
        send_req = requests.get(url, verify=False, headers=headers)
        if send_req.status_code != 200:
            return JsonResponse({'error': 'code invalid'})
        documentNumber_position_raw = send_req.text.find('证件号码')
        documentNumber_position_start = send_req.text.find('class="cnt1">', documentNumber_position_raw) + 13
        documentNumber_position_end = send_req.text.find('</div>', documentNumber_position_start)
        documentNumber_true = send_req.text[documentNumber_position_start:documentNumber_position_end]
        if documentNumber == documentNumber_true:
            user = User.objects.filter(username=username)
            if len(user) > 0:
                user.qualificationStatus = "Qualified"
                user.documentNumber = documentNumber
                user.save()
            else:
                return JsonResponse({'error': 'user does not exist'})
        else:
            return JsonResponse({'error': 'wrong document number'})
        return JsonResponse({'message': 'ok'})
    return JsonResponse({'error': 'need POST method'})


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
