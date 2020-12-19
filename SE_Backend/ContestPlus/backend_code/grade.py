import csv
import os
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from ContestPlus.backend_code.secure import *


def api_grade_sheet(request):
    if request.method == 'POST':
        post = eval(request.body)
        us_type, _ = user_type(request)
        if us_type == 'error':
            return JsonResponse({'error': 'login'})
        if us_type != 'sponsor':
            return JsonResponse({'error': 'authority'})
        try:
            contest = Contest.objects.get(id=post['contestId'])
            if contest.censorStatus != 'accept':
                return JsonResponse({'error': 'status'})
        except Contest.DoesNotExist:
            return JsonResponse({'error': 'contest'})
        retrieve_participant = Participation.objects.filter(
            targetContestId=post['contestId'], checkStatus='accept')
        response = {'count': len(retrieve_participant), 'data': []}
        for i in retrieve_participant:
            if os.path.isfile(i.submissionDir) and i.grade != '':
                i.completeStatus = 'completing'
                i.save()
        if contest.allowGroup:
            retrieve_participant = retrieve_participant\
                .values('participantId', 'completeStatus', 'grade', 'mainAward',
                        'extraAward').distinct()
            response['count'] = len(retrieve_participant)
            for i in retrieve_participant:
                group = Group.objects.get(id=i['participantId'])
                participant = {'participantId': i['participantId'],
                               'name': group.name, 'submitted': 1 if
                               i['completeStatus'] == 'completed' else 0,
                               'grade': i['grade'], 'mainAward': i['mainAward'],
                               'extraAward': i['extraAward']}
                response['data'].append(participant)
        else:
            for i in retrieve_participant:
                user = User.objects.get(id=i.userId)
                participant = {'participantId': user.id, 'name': user.trueName,
                               'submitted': 1 if i.completeStatus == 'completed'
                               else 0, 'mainAward': i.mainAward,
                               'grade': i.grade, 'extraAward': i.extraAward}
                response['data'].append(participant)
        return JsonResponse(response)
    return JsonResponse({'error': 'need POST method'})


def api_grade_download(request):
    if request.method == 'POST':
        post = eval(request.body)
        us_type, _ = user_type(request)
        if us_type == 'error':
            return JsonResponse({'error': 'login'})
        if us_type != 'sponsor':
            return JsonResponse({'error': 'authority'})
        try:
            contest = Contest.objects.get(id=post['contestId'])
            if contest.censorStatus != 'accept':
                return JsonResponse({'error': 'status'})
        except Contest.DoesNotExist:
            return JsonResponse({'error': 'contest'})
        retrieve_participant = Participation.objects.filter(
            targetContestId=post['contestId'], checkStatus='accept')
        file = str(settings.BASE_DIR) + '/files/needPermission/grade/' +\
               str(contest.id) + '/' + str(contest.id) + '_' +\
               contest.title + '.csv'
        f = open(file, 'w', newline='')
        writer = csv.writer(f)
        writer.writerow(['报名ID', '队名' if contest.allowGroup else '姓名', '是'
                         '否提交', '打分', '主要奖项', '次要奖项 多个请以空格分割'])
        if contest.allowGroup:
            retrieve_participant = retrieve_participant\
                .values('participantId', 'completeStatus', 'grade', 'mainAward',
                        'extraAward').distinct()
            for i in retrieve_participant:
                group = Group.objects.get(id=i['participantId'])
                writer.writerow([i['participantId'], group.name, '是' if
                               i['completeStatus'] == 'completed' else '否',
                               i['grade'], i['mainAward'], i['extraAward']])
        else:
            for i in retrieve_participant:
                user = User.objects.get(id=i.userId)
                writer.writerow([user.id, user.trueName,
                                 '是' if i.completeStatus == 'completed'
                                 else '否', i.grade, i.mainAward,
                                 i.extraAward])
        f.close()
        response = HttpResponse(status=200)
        response['Content-Disposition'] = 'attachment; filename=%s' % file
        response['Content-Type'] = 'application/octet-stream'
        response['X-Accel-Redirect'] = '/file/grade/' + str(contest.id) + '/' +\
                                       str(contest.id) + '_' +\
                                       contest.title + '.csv'
        return response
    return JsonResponse({'error': 'need POST method'})


def api_grade_upload(request):
    if request.method == 'POST':
        post = eval(request.body)
        us_type, _ = user_type(request)
        if us_type == 'error':
            return JsonResponse({'error': 'login'})
        if us_type != 'sponsor':
            return JsonResponse({'error': 'authority'})
        try:
            contest = Contest.objects.get(id=post['contestId'])
            if contest.censorStatus != 'accept' or contest.publishResult:
                return JsonResponse({'error': 'status'})
        except Contest.DoesNotExist:
            return JsonResponse({'error': 'contest'})
        stream = request.FILES.get(post['file_key'], None)
        file = str(settings.BASE_DIR) + '/files/needPermission/grade/' +\
               str(contest.id) + '/' + str(contest.id) + '_' +\
               contest.title + '.csv'
        csv_w = open(file, 'wb+')
        for i in stream.chunks():
            csv_w.write(i)
        csv_w.close()
        csv_r = open(file, 'r')
        reader = csv.reader(csv_r)
        for i, row in enumerate(reader):
            if i:
                participant = Participation.objects\
                    .filter(participantId=int(row[0]),
                            targetContestId=contest.id)
                for item in participant:
                    if row[3] and row[3] != '':
                        try:
                            _ = int(row[3])
                            item.grade = row[3]
                        except ValueError:
                            continue
                    if row[4]:
                        if len(row[4]) > 20:
                            item.mainAward = row[4][: 20]
                        else:
                            item.mainAward = row[4]
                    if row[5]:
                        if len(row[5]) > 20:
                            item.extraAward = row[5][: 20]
                        else:
                            item.extraAward = row[5]
                    item.save()
        csv_r.close()
        return JsonResponse({'message': 'ok'})
    return JsonResponse({'error': 'need POST method'})


def api_grade_submit_sheet(request):
    if request.method == 'POST':
        post = eval(request.body)
        us_type, _ = user_type(request)
        if us_type == 'error':
            return JsonResponse({'error': 'login'})
        if us_type != 'sponsor':
            return JsonResponse({'error': 'authority'})
        try:
            contest = Contest.objects.get(id=post['contestId'])
            if contest.censorStatus != 'accept' or contest.publishResult:
                return JsonResponse({'error': 'status'})
        except Contest.DoesNotExist:
            return JsonResponse({'error': 'contest'})
        data = post['data']
        for i in range(post['count']):
            participant = Participation.objects.filter(participantId=
                                                       data[i]['participantId'])
            for j in participant:
                j.grade = data[i]['grade']
                j.mainAward = data[i]['mainAward']
                j.extraAward = data[i]['extraAward']
                j.save()
        if post['publish']:
            contest.publishResult = 1
            contest.save()
        return JsonResponse({'message': 'ok'})
    return JsonResponse({'error': 'need POST method'})