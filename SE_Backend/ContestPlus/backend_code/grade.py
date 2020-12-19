import csv
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
