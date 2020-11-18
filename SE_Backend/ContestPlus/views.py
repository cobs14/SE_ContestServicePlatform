from django.shortcuts import render
import random
from django.http import JsonResponse
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail
from .models import User
from .models import EmailCode
from .models import Sponsor


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
        code=random_str()
        email_code = EmailCode.objects.filter(userId=new_user.id)
        if len(email_code) > 0:
            new_email_code=email_code[0]
        else:
            new_email_code = EmailCode(userId=new_user.id, userType=0, code=code)
        # now_time = timezone.now()
        # print(now_time)
        # if new_email_code.sendTime.hour + 60 > now_time:
        #     return JsonResponse({"error": "email still valid"})
        new_email_code.save()
        send_message = "Your verification link is \n" + 'http://127.0.0.1:8000/register/verification/' + code#本机调试版
        send_mail("Contest Plus Email Verification", send_message, settings.DEFAULT_FROM_EMAIL, [email])
        return JsonResponse({"message": "ok"})


def random_str():
    _str = '1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    return ''.join(random.choice(_str) for i in range(8))


def apiRegisterVerifyMail(request):
    if request.method == 'POST':
        post = request.POST
        if post.get('code'):
            try:
                email_code = EmailCode.objects.get(code=post['code'])
                if email_code.sendTime = 
            except EmailCode.DoesNotExist:
                return JsonResponse({'message': 'no such a code'})
        else:
            return JsonResponse({'message': 'blank request'})
    return JsonResponse({'message': 'need POST method'})


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

