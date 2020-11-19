from django.shortcuts import render
import random
import time
import datetime
from django.http import JsonResponse
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail
from .models import User
from .models import EmailCode
from .models import Sponsor
from .models import Contest


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
        new_user.email = email
        new_user.save()

        # 发送邮件
        code = random_str()
        email_code = EmailCode.objects.filter(userId=new_user.id)
        if len(email_code) > 0:
            new_email_code = email_code[0]
        else:
            new_email_code = EmailCode(userId=new_user.id, userType='user', code=code)
            now_time = datetime.datetime.now()
            un_time = time.mktime(now_time.timetuple())
            un_time2 = time.mktime(new_email_code.sendTime.timetuple())
            if un_time2 + 60 > un_time:
                return JsonResponse({"error": "email still valid"})
        new_email_code.save()
        send_message = "Your verification link is \n" + 'http://127.0.0.1:8000/register/verification/' + code  # 本机调试版
        send_mail("Contest Plus Email Verification", send_message, settings.DEFAULT_FROM_EMAIL, [email])
        return JsonResponse({"message": "ok"})


def random_str():
    _str = '1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    return ''.join(random.choice(_str) for i in range(8))


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

        module = params['module']
        if len(module) > 0:
            module_retrieved_contest = Contest.objects.none()
            for z in module:
                module_retrieve_step = retrieved_contest.filter(module__contains=z)
                module_retrieved_contest = module_retrieved_contest | module_retrieve_step
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
                description_text_retrieved_contest = description_text_retrieved_contest.union\
                    (description_text_retrieved_step)
            retrieved_contest = title_text_retrieved_contest.union\
                (abstract_text_retrieved_contest, description_text_retrieved_contest)

        state = params['state']
        apply = state['apply']
        contest = state['contest']
        review = state['review']

        # if apply != 0:
        #     if apply == 1:
        #
        #     if apply == 2:
        #
        #     if apply == 3:
        #
        # if contest !=0:
        #     if contest == 1:
        #
        #     if contest == 2:
        #
        #     if contest == 3:
        #
        # if review !=0:
        #     if review == 1:
        #
        #     if review == 2:
        #
        #     if review == 3:
        if pageNum == 0 or pageSize ==0:
            start_pos = 0
            end_pos = len(retrieved_contest)
        else:
            start_pos = (pageNum-1)*pageSize
            end_pos = pageNum*pageSize
        response_contest = []
        for z in retrieved_contest[start_pos:end_pos]:
            response_contest_ele = {}
            response_contest_ele['id'] = z.id
            response_contest_ele['title'] = z.title
            sponsor = Sponsor.objects.filter(id=z.sponsorId)
            response_contest_ele['sponsor'] = sponsor[0].sponsorName
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
        response = {}
        response['count'] = len(response_contest)
        response['data'] = response_contest
        return JsonResponse(response)


def apiRegisterVerifyMail(request):
    return


#     if request.method == 'POST':
#         post = request.POST
#         if post.get('code'):
#             try:
#                 email_code = EmailCode.objects.get(code=post['code'])
#                 if email_code.sendTime =
#             except EmailCode.DoesNotExist:
#                 return JsonResponse({'message': 'no such a code'})
#         else:
#             return JsonResponse({'message': 'blank request'})
#     return JsonResponse({'message': 'need POST method'})


def apiKey(request):
    if request.method == 'POST':
        post = request.POST
        user = None
        if post.get('username'):
            try:
                user = User.objects.get(username=post['username'])
            except User.DoesNotExist:
                return JsonResponse({'message': 'no such a user'})
        elif post.get('email'):
            try:
                user = User.objects.get(username=post['email'])
            except User.DoesNotExist:
                return JsonResponse({'message': 'no such a user'})
        if user:
            if user.emailVerifyStatus:
                return JsonResponse({'message': 'ok', 'key': user.pubkey})
            else:
                return JsonResponse({'message': 'need verification'})
        return JsonResponse({'message': 'blank request'})
    return JsonResponse({'message': 'need POST method'})


def apiLogin(request):
    if request.method == 'POST':
        post = request.POST