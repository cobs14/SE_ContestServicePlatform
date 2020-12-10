import datetime
import rsa
import hashlib
import requests
from django.http import JsonResponse
from django.conf import settings
from django.core.mail import send_mail
from ContestPlus.backend_code.secure import *

false = False
true = True


def apiGenerateInvitationCode(request):
    if request.method == 'POST':
        try:
            request_body = eval(request.body)
            true_name = request_body.get('trueName')
        except:
            return JsonResponse({"error": "invalid parameters"})
        usertype, _ = user_type(request)
        if usertype != 'admin':
            return JsonResponse({"error": "not admin"})
        code_length = 16
        code = random_str(code_length)
        new_invitation_code = InvitationCode(code=code, valid=True, username=true_name)
        new_invitation_code.save()
        return JsonResponse({'code': code})
    return JsonResponse({'error': 'need POST method'})


def apiBrowseInvitationCode(request):
    if request.method == 'POST':
        # 处理重复情况
        usertype, _ = user_type(request)
        if usertype != 'admin':
            return JsonResponse({"error": "not admin"})
        invatation_code=InvitationCode.objects.all()
        return_data = {}
        return_data_list=[]
        for z in invatation_code:
            code_ele={}
            code_ele['codeId']=z.id
            code_ele['codeText']=z.code
            code_ele['valid']=z.valid
            code_ele['username']=z.username
            return_data_list.append(code_ele)
        return_data['count']=len(invatation_code)
        return_data['data']=return_data_list
        return JsonResponse(return_data)
    return JsonResponse({'error': 'need POST method'})


def apiRegister(request):
    if request.method == 'POST':
        try:
            request_body = eval(request.body)
            username = request_body.get('username')
            password = request_body.get('password')
            email = request_body.get('email')
            usertype = request_body.get('userType')
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
        if usertype == 'sponsor':
            try:
                invitation_code = request_body.get('userType')
                true_name = request_body.get('trueName')
            except:
                return JsonResponse({"error": "no code"})
            true_code = InvitationCode.objects.filter(code=invitation_code)
            if len(true_code) > 0 and true_code[0].valid is True:
                new_user.userType = 'sponsor'
                new_user.trueName = true_name
                true_code[0].valid = False
            else:
                return JsonResponse({"error": "code invalid"})
        else:
            new_user.userType = 'guest'
        new_user.save()

        # 发送邮件
        code_length = 8
        code = random_str(code_length)
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
                                 'email': user.email})
        else:
            return JsonResponse({'error': 'wrong password'})
    return JsonResponse({'error': 'need POST method'})


def apiQualification(request):
    if request.method == 'POST':
        usertype, _ = user_type(request)
        if usertype == 'error':
            return JsonResponse({'error': 'login'})
        if usertype != 'guest':
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
                user.userType = "user"

                user.documentNumber = documentNumber
                next_year_time = datetime.datetime.now() + datetime.timedelta(days=365)
                user.OutdateTime.year = next_year_time
                user.save()
            else:
                return JsonResponse({'error': 'user does not exist'})
        else:
            return JsonResponse({'error': 'wrong document number'})
        return JsonResponse({'message': 'ok'})
    return JsonResponse({'error': 'need POST method'})


def apiReset(request):
    if request.method == 'POST':
        try:
            post = eval(request.body)
            email = post.get('email')
            user = User.objects.get(email=email)
        except:
            return JsonResponse({"error": "invalid parameter"})

        # 发送邮件
        code_length = 8
        code = random_str(code_length)
        email_code = EmailCode.objects.filter(userId=user.id)
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
            new_email_code = EmailCode(userId=user.id, userType=user.userType, code=code)
            new_email_code.save()
        send_message = "Your reset link is \n" + 'http://127.0.0.1:8080/reset/' + code  # 本机调试版
        send_mail("Contest Plus Password Reset", send_message, settings.DEFAULT_FROM_EMAIL, [email])
        return JsonResponse({"message": "ok"})
    return JsonResponse({'error': 'need POST method'})


def apiResetCode(request):
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
                return response
            except EmailCode.DoesNotExist:
                return JsonResponse({'error': 'no such a code'})
        else:
            return JsonResponse({'error': 'blank request'})
    return JsonResponse({'error': 'need POST method'})


def apiResetPassword(request):
    if request.method == 'POST':
        post = eval(request.body)
        if post.get('code'):
            try:
                response = JsonResponse({'message': 'ok'})
                email_code = EmailCode.objects.get(code=post['code'])
                user = User.objects.get(id=email_code.userId)
                user.password = post['password']
                user.save()
                return response
            except EmailCode.DoesNotExist:
                return JsonResponse({'error': 'no such a code'})
        else:
            return JsonResponse({'error': 'blank request'})
    return JsonResponse({'error': 'need POST method'})
