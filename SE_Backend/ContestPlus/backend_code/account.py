import datetime
import rsa
import hashlib
import requests
import os
from django.http import JsonResponse
from django.conf import settings
from django.core.mail import send_mail
from ContestPlus.backend_code.secure import *
from ContestPlus.backend_code.contact import send_system_message
from aip import AipOcr

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
        invitation_code = InvitationCode.objects.all()
        return_data = {}
        return_data_list = []
        for z in invitation_code:
            code_ele = {'codeId': z.id, 'codeText': z.code, 'valid': z.valid,
                        'trueName': z.username}
            return_data_list.append(code_ele)
        return_data['count'] = len(invitation_code)
        return_data['data'] = return_data_list
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
                invitation_code = request_body.get('invitationCode')
            except:
                return JsonResponse({"error": "no code"})
            true_code = InvitationCode.objects.filter(code=invitation_code)
            if len(true_code) > 0 and true_code[0].valid is True:
                true_name=true_code[0].username
                new_user.userType = 'sponsor'
                new_user.trueName = true_name
                true_code[0].valid = False
                true_code[0].save()
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
                    if user.userType == 'guest':
                        update_group_code(user.id)
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
                                 'email': user.email, 'avatar': user.avatar})
        else:
            return JsonResponse({'error': 'wrong password'})
    return JsonResponse({'error': 'need POST method'})


def apiQualification(request):
    if request.method == 'POST':
        usertype, user = user_type(request)
        if usertype == 'error':
            return JsonResponse({'error': 'login'})
        if usertype != 'guest':
            return JsonResponse({'error': 'authority'})
        try:
            request_body = eval(request.body)
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

        school_position_raw = send_req.text.find('院校')
        school_position_start = send_req.text.find('class="cnt1">', school_position_raw) + 13
        school_position_end = send_req.text.find('</div>', school_position_start)
        school_true = send_req.text[school_position_start:school_position_end]

        major_position_raw = send_req.text.find('专业')
        major_position_start = send_req.text.find('class="cnt1">', major_position_raw) + 13
        major_position_end = send_req.text.find('</div>', major_position_start)
        major_true = send_req.text[major_position_start:major_position_end]

        studentNumber_position_raw = send_req.text.find('学号')
        studentNumber_position_start = send_req.text.find('class="cnt1">', studentNumber_position_raw) + 13
        studentNumber_position_end = send_req.text.find('</div>', studentNumber_position_start)
        studentNumber_true = send_req.text[studentNumber_position_start:studentNumber_position_end]

        # birthTime_position_raw = send_req.text.find('出生日期')
        # birthTime_position_start = send_req.text.find('class="cnt1">', birthTime_position_raw) + 13
        # birthTime_position_end = send_req.text.find('</div>', birthTime_position_start)
        # birthTime_true = send_req.text[birthTime_position_start:birthTime_position_end]

        nameImage_position_start = send_req.text.find('class="by_img"') + 20
        nameImage_position_end = send_req.text.find('\"', nameImage_position_start)
        nameImage_true = send_req.text[nameImage_position_start:nameImage_position_end]

        url_prefix = 'https://www.chsi.com.cn'
        url = url_prefix + nameImage_true
        trueName = image2text(url)
        if trueName == '':
            return JsonResponse({'error': '验证码无效'})
        md5 = hashlib.md5()
        md5.update((documentNumber + school_true).encode('utf-8'))
        idNumber = md5.hexdigest()
        try:
            _ = User.objects.get(school=school_true, idNumber=idNumber)
            return JsonResponse({'error': 'already exists'})
        except User.DoesNotExist:
            pass
        if documentNumber == documentNumber_true:
            user.userType = "user"
            user.documentNumber = documentNumber[: 4] + '****'\
                                                      + documentNumber[-2:]

            user.idNumber = idNumber
            # user.birthTime = birthTime_true
            user.school = school_true
            user.studentNumber = studentNumber_true
            user.major = major_true
            user.trueName = trueName

            # next_year_time = datetime.datetime.now() + datetime.timedelta(days=365)
            # user.OutdateTime.year = next_year_time
            user.save()
        else:
            return JsonResponse({'error': 'wrong document number'})
        send_system_message('您的实名验证已通过。', user.id)
        return JsonResponse({'message': 'ok'})
    return JsonResponse({'error': 'need POST method'})


APP_ID = '23152764'
API_KEY = 'lacjkNZceCRkO8ItUQM7OkfR'
SECRET_KEY = 'Oe80o95YoZKebKoOIoLwhoKCgO38Grgf'
client = AipOcr(APP_ID, API_KEY, SECRET_KEY)


def image2text(image):
    dic_result = client.webImageUrl(image)
    # print(dic_result)
    try:
        res = dic_result['words_result']
        result = ''
        for m in res:
            result = result + str(m['words'])
    except:
        result = ''
    return result


def apiQualificationManual(request):
    if request.method == 'POST':
        try:
            file_key = request.POST.get('fileKey')
            file = request.FILES.get(file_key, None)
        except:
            return JsonResponse({"error": "invalid parameters"})
        userType,user = user_type(request)
        manual_qual=ManualQualification.objects.filter(userId=user.id)
        if len(manual_qual) >0:
            return JsonResponse({"error":"now pending"})

        file_dir = checkPlatform(str(settings.BASE_DIR) + "/files/manualQualify/" + str(user.id) + "/")
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)

        new_manual_qual=ManualQualification\
            (userId=user.id,fileDir=file_dir,fileName=file.name,result='pending')
        new_manual_qual.save()

        destination = open(os.path.join(file_dir, file.name), 'wb+')
        for chunk in file.chunks():
            destination.write(chunk)
        destination.close()

        return JsonResponse({'message': 'ok'})
    return JsonResponse({'error': 'need POST method'})


def apiQualificationFetch(request):

    return


def apiQualificationFile(request):
    return


def apiQualificationVerify(request):
    return


def apiReset(request):
    if request.method == 'POST':
        try:
            post = eval(request.body)
            email = post.get('email')
            user = User.objects.get(email=email)
            if not user.emailVerifyStatus:
                return JsonResponse({"error": "email"})
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
        send_message = "Your reset link is \n" + 'http://127.0.0.1:8080/resetpassword/' + code  # 本机调试版
        send_mail("Contest Plus Password Reset", send_message, settings.DEFAULT_FROM_EMAIL, [email])
        return JsonResponse({"message": "ok"})
    return JsonResponse({'error': 'need POST method'})


def apiResetCode(request):
    if request.method == 'POST':
        post = eval(request.body)
        if post.get('code'):
            try:
                email_code = EmailCode.objects.get(code=post['code'])
                now_time = datetime.datetime.now()
                un_time = time.mktime(now_time.timetuple())
                un_time2 = time.mktime(email_code.sendTime.timetuple())
                if un_time2 + 3600 < un_time:
                    response = JsonResponse({'error': 'code outdated'})
                user = User.objects.get(id=email_code.userId)
                response = JsonResponse({'message': 'ok', 'username': user.username})
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
                email_code.delete()
                return response
            except EmailCode.DoesNotExist:
                return JsonResponse({'error': 'no such a code'})
        else:
            return JsonResponse({'error': 'blank request'})
    return JsonResponse({'error': 'need POST method'})

