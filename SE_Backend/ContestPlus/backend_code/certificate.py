from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import zipfile
from ContestPlus.backend_code.secure import *
from django.conf import settings
from django.http import JsonResponse, HttpResponse
import qrcode
import os
from SE_Backend import settings


# 根据所给信息动态生成奖状
def generate(award, user, sponsor, contest, index, zip_file, verify_code):
    image = Image.open(
        str(settings.BASE_DIR) + "/CertificationModel/certification_model.png")
    draw = ImageDraw.Draw(image)
    name_text = user.trueName + ":"
    contest_text_part1 = "恭喜你在" + sponsor.trueName + "举办的"
    contest_text_part2 = contest.title + "中获得"
    award_text = award
    sponsor_text = sponsor.trueName
    time_text = contest.publishResult
    qrcode_text = "扫描二维码验证："
    host_name = settings.host + '/certificate/'

    name_position = (380 - 36 * (len(name_text) - 1), 565)
    name_font = ImageFont.truetype(
        str(settings.BASE_DIR) + '/CertificationModel/STXINWEI.TTF', 72)
    draw.text(name_position, name_text, font=name_font, fill='white')

    contest_position_part1 = (1000 - 25 * (len(contest_text_part1)), 640)
    contest_font_part1 = ImageFont.truetype(
        str(settings.BASE_DIR) + '/CertificationModel/STZHONGS.TTF', 50)
    draw.text(contest_position_part1, contest_text_part1,
              font=contest_font_part1, fill='white')

    contest_position_part2 = (1000 - 25 * (len(contest_text_part2)), 710)
    contest_font_part2 = ImageFont.truetype(
        str(settings.BASE_DIR) + '/CertificationModel/STZHONGS.TTF', 50)
    draw.text(contest_position_part2, contest_text_part2,
              font=contest_font_part2, fill='white')

    award_position = (1000 - 50 * (len(award_text)), 780)
    award_font = ImageFont.truetype(
        str(settings.BASE_DIR) + '/CertificationModel/STZHONGS.TTF', 100)
    draw.text(award_position, award_text, font=award_font, fill='white')

    sponsor_position = (1600 - 18 * (len(sponsor_text)), 1100)
    sponsor_font = ImageFont.truetype(
        str(settings.BASE_DIR) + '/CertificationModel/STZHONGS.TTF', 36)
    draw.text(sponsor_position, sponsor_text, font=sponsor_font, fill='white')

    time_position = (1600 - 18 * (len(time_text) - 3), 1150)
    time_font = ImageFont.truetype(
        str(settings.BASE_DIR) + '/CertificationModel/STZHONGS.TTF', 36)
    draw.text(time_position, time_text, font=time_font, fill='white')

    qrcode_position = (1005 - 18 * (len(qrcode_text)), 950)
    qrcode_font = ImageFont.truetype(
        str(settings.BASE_DIR) + '/CertificationModel/STZHONGS.TTF', 36)
    draw.text(qrcode_position, qrcode_text, font=qrcode_font, fill='white')
    qr = qrcode.QRCode(version=5,
                       error_correction=qrcode.constants.ERROR_CORRECT_L,
                       box_size=10, border=4, )
    qr.add_data(host_name + verify_code)
    qr.make(fit=True)
    qr_img = qr.make_image()
    qr_img = qr_img.resize((200, 200))
    image.paste(qr_img, (900, 1020))
    image_dir = str(settings.BASE_DIR) + "/files/needPermission/" \
                                         "certificate/" + str(contest.id) \
                + '/' + str(user.id) + '_' + user.trueName + '/'
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)
    image.save(image_dir + str(index) + '.png')
    zip_file.write(image_dir + str(index) + '.png', str(index) + '.png')


# 竞赛举办者批量下载证书
def apiCertificationGet(request):
    if request.method == 'POST':
        post = eval(request.body)
        us_type, sponsor = user_type(request)
        if us_type == 'error':
            return JsonResponse({'error': 'login'})
        if us_type != 'sponsor':
            return JsonResponse({'error': 'authority'})
        try:
            contest = Contest.objects.get(id=post['contestId'])
            if contest.censorStatus != 'accept' or contest.publishResult == '':
                return JsonResponse({'error': 'status'})
            if contest.sponsorId != sponsor.id:
                return JsonResponse({'error': 'authority'})
        except Contest.DoesNotExist:
            return JsonResponse({'error': 'contest'})
        retrieved_participant = Participation.objects\
            .filter(targetContestId=contest.id)
        if post['count'] > 0:
            tmp = retrieved_participant.filter(participantId=
                                               post['participantId'][0])
            for i in post['participantId'][1:]:
                tmp = tmp | retrieved_participant.filter(participantId=i)
            retrieved_participant = tmp
        outer_zip_dir = str(settings.BASE_DIR) + "/files/needPermission/certificate/"
        if not os.path.exists(outer_zip_dir):
            os.makedirs(outer_zip_dir)
        outer_zip_name = outer_zip_dir + str(contest.id) + '.zip'
        outer_zip_file = zipfile.ZipFile(outer_zip_name, "w", zipfile.ZIP_DEFLATED)
        for i in retrieved_participant:
            user = User.objects.get(id=i.userId)
            imgs = [i.mainAward] + (i.extraAward.split(' ') if len(i.extraAward) > 0 else [])
            if len(imgs) == 0:
                continue
            zip_dir = str(settings.BASE_DIR) + "/files/needPermission/certificate/" +\
                      str(contest.id) + "/"
            if not os.path.exists(zip_dir):
                os.makedirs(zip_dir)
            zip_name = zip_dir + str(user.id) + '.zip'
            if i.verifyCode == '':
                i.verifyCode = random_str(32)
                i.save()
            else:
                if os.path.exists(zip_name):
                    outer_zip_file.write(zip_name, str(
                        user.id) + '_' + user.trueName + '.zip')
                    continue
            zip_file = zipfile.ZipFile(zip_name, "w", zipfile.ZIP_DEFLATED)
            for j, award in enumerate(imgs):
                generate(award, user, sponsor, contest, j, zip_file,
                         i.verifyCode)
            zip_file.close()
            outer_zip_file.write(zip_name, str(user.id) + '_' + user.trueName + '.zip')
        outer_zip_file.close()
        response = HttpResponse(status=200)
        response['Content-Disposition'] = 'attachment; filename=%s' % str(
            contest.id) + ".zip"
        response['Content-Type'] = 'application/octet-stream'
        response['X-Accel-Redirect'] = '/file/certificate/' + str(contest.id) + ".zip"
        return response
    return JsonResponse({'error': 'need POST method'})


# 参赛者下载个人证书
def apiCertificationGetMy(request):
    if request.method == 'POST':
        post = eval(request.body)
        us_type, user = user_type(request)
        if us_type == 'error':
            return JsonResponse({'error': 'login'})
        if us_type != 'user':
            return JsonResponse({'error': 'authority'})
        try:
            contest = Contest.objects.get(id=post['contestId'])
            if contest.censorStatus != 'accept' or contest.publishResult == '':
                return JsonResponse({'error': 'status'})
        except Contest.DoesNotExist:
            return JsonResponse({'error': 'contest'})
        retrieved_participant = Participation.objects\
            .filter(targetContestId=contest.id, userId=user.id)
        if len(retrieved_participant) != 1:
            return JsonResponse({'error': 'apply'})
        for i in retrieved_participant[0: 1]:
            user = User.objects.get(id=i.userId)
            imgs = [i.mainAward] + (i.extraAward.split(' ') if len(i.extraAward) > 0 else [])
            if len(imgs) == 0:
                break
            zip_dir = str(settings.BASE_DIR) + "/files/needPermission/certificate/" +\
                      str(contest.id) + "/"
            if not os.path.exists(zip_dir):
                os.makedirs(zip_dir)
            zip_name = zip_dir + str(user.id) + '.zip'
            if i.verifyCode == '':
                i.verifyCode = random_str(32)
                i.save()
            else:
                if os.path.exists(zip_name):
                    break
            zip_file = zipfile.ZipFile(zip_name, "w", zipfile.ZIP_DEFLATED)
            sponsor = User.objects.get(id=contest.sponsorId)
            for j, award in enumerate(imgs):
                generate(award, user, sponsor, contest, j, zip_file,
                         i.verifyCode)
            zip_file.close()
        response = HttpResponse(status=200)
        response['Content-Disposition'] = 'attachment; filename=%s' % str(
            user.id) + ".zip"
        response['Content-Type'] = 'application/octet-stream'
        response['X-Accel-Redirect'] = '/file/certificate/' + str(contest.id) + '/' + str(user.id) + '.zip'
        return response
    return JsonResponse({'error': 'need POST method'})


# 参赛者查看个人奖项
def apiCertificationAward(request):
    if request.method == 'POST':
        post = eval(request.body)
        us_type, user = user_type(request)
        if us_type == 'error':
            return JsonResponse({'error': 'login'})
        if us_type != 'user':
            return JsonResponse({'error': 'authority'})
        try:
            contest = Contest.objects.get(id=post['contestId'])
            if contest.censorStatus != 'accept' or contest.publishResult == '':
                return JsonResponse({'error': 'status'})
        except Contest.DoesNotExist:
            return JsonResponse({'error': 'contest'})
        participant = Participation.objects\
            .filter(targetContestId=contest.id, userId=user.id)
        if len(participant) != 1:
            return JsonResponse({'error': 'apply'})
        return JsonResponse({'mainAward': participant[0].mainAward, 'extraAward':
            participant[0].extraAward, 'verifyCode': participant[0].verifyCode})
    return JsonResponse({'error': 'need POST method'})


# 扫描二维码验证奖项信息
def apiCertificationVerify(request):
    if request.method == 'POST':
        post = eval(request.body)
        try:
            participant = Participation.objects.get(verifyCode=
                                                    post['verifyCode'])
            contest = Contest.objects.get(id=participant.targetContestId)
            sponsor = User.objects.get(id=contest.sponsorId)
            award = participant.mainAward
            if award != '' and participant.extraAward != '':
                award += ' ' + participant.extraAward
            else:
                award += participant.extraAward
            response = {'contestInfo': {'issueDate': contest.publishResult,
                                        'contestId': contest.id, 'contestName':
                                        contest.title, 'allowGroup': 1 if
                                        contest.allowGroup else 0, 'award':
                                        award},
                        'sponsorInfo': {'userId': sponsor.id, 'trueName':
                                        sponsor.trueName},
                        'participantInfo': {}}
            member = [str(participant.userId)]
            response['participantInfo']['participants'] = []
            if contest.allowGroup:
                group = Group.objects.get(id=participant.participantId)
                response['participantInfo']['groupName'] = group.name
                member = group.memberId.split(',')
            for i in member:
                user = User.objects.get(id=int(i))
                response['participantInfo']['participants'].append({
                    'id': user.id, 'username': user.username, 'trueName':
                    user.trueName, 'school': user.school, 'major': user.major,
                    'documentId': user.documentNumber
                })
            return JsonResponse(response)
        except Participation.DoesNotExist:
            return JsonResponse({'error': 'invalid code'})
    return JsonResponse({'error': 'need POST method'})
