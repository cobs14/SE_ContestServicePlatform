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
        response = {'count': 'single', 'list': []}
        if contest.allowGroup:
            response['type'] = 'group'
            retrieve_participant = retrieve_participant.values('participantId')\
                .distinct()
            for i in retrieve_participant:
                group = Group.objects.get(id=i['participantId'])
                participant = {'groupId': i['participantId'],
                               'groupName': group.name,
                               'description': group.description,
                               'memberCount': group.memberCount, 'member': []}
                s = group.memberId.split(',')
                for j in s:
                    user = User.objects.get(id=int(j))
                    participant['member'].append({'userId': user.id,
                                                  'email': user.email,
                                                  'username': user.username,
                                                  'trueName': user.trueName,
                                                  'school': user.school,
                                                  'major': user.major,
                                                  'avatar': user.avatar})
                response['list'].append(participant)
        else:
            for i in retrieve_participant:
                user = User.objects.get(id=i.userId)
                participant = {'userId': user.id, 'username': user.username,
                               'trueName': user.trueName, 'school': user.school,
                               'major': user.major, 'email': user.email,
                               'avatar': user.avatar}
                response['list'].append(participant)
        return JsonResponse(response)
    return JsonResponse({'error': 'need POST method'})
