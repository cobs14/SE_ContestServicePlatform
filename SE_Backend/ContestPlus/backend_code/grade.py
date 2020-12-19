from django.http import JsonResponse
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
