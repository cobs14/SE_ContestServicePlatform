from django.http import JsonResponse
from ContestPlus.backend_code.secure import *


def apiUserContact(request):
    if request.method == 'POST':
        post = eval(request.body)
        utype, user = user_type(request)
        if utype == 'error':
            return JsonResponse({'error': 'login'})
        pageNum = post['pageNum']
        pageSize = post['pageSize']
        retrieved_dialog = Dialog.objects.filter(receiver=user.id).order_by('-updateTime')
        if pageNum == 0 or pageSize == 0:
            start_pos = 0
            end_pos = len(retrieved_dialog)
        else:
            start_pos = (pageNum - 1) * pageSize
            end_pos = pageNum * pageSize
        response = {'contact': retrieved_dialog[start_pos: end_pos]}
        return JsonResponse(response)
    return JsonResponse({'error': 'need POST method'})


def apiUser(request):
    if request.method == 'POST':
        post = eval(request.body)
        utype, user = user_type(request)
        if utype == 'error':
            return JsonResponse({'error': 'login'})
        response = {'id': user.id, 'username': user.username,
                    'email': user.email, 'documentNumber': user.documentNumber,
                    'avatar': user.avatar, 'userType': user.userType}
        return JsonResponse(response)
    return JsonResponse({'error': 'need POST method'})


def apiUserRetrieve(request):
    if request.method == 'POST':
        try:
            post = eval(request.body)
            params = post.get('params')
            pageNum = post.get('pageNum')
            pageSize = post.get('pageSize')
        except:
            return JsonResponse({"error": "invalid parameters"})
        retrieved_user = User.objects.filter(userType=params['userType'],
                                             emailVerifyStatus=1)

        username = params['username']
        if len(username) > 0:
            retrieved_user = retrieved_user.filter(username__contains=username)
        school = params['school']
        if len(school) > 0:
            retrieved_user = retrieved_user.filter(school__contains=school)
        major = params['major']
        if len(major) > 0:
            retrieved_user = retrieved_user.filter(major__contains=major)
        studentNumber = params['studentNumber']
        if len(studentNumber) > 0:
            retrieved_user = retrieved_user.filter(studentNumber__contains=studentNumber)

        if pageNum <= 0 or pageSize <= 0:
            start_pos = 0
            end_pos = len(retrieved_user)
        else:
            start_pos = (pageNum - 1) * pageSize
            end_pos = pageNum * pageSize
        response = {}
        response['count'] = retrieved_user.count()
        response_user = []
        for z in retrieved_user[start_pos:end_pos]:
            response_user_ele = {}
            response_user_ele['id'] = z.id
            response_user_ele['username'] = z.username
            response_user_ele['avatar'] = z.avatar
            response_user_ele['school'] = z.school
            response_user_ele['major'] = z.major
            response_user.append(response_user_ele)

        response['data'] = response_user
        return JsonResponse(response)
    return JsonResponse({'error': 'need POST method'})


def apiUserCheckRelation(request):
    if request.method == 'POST':
        post = eval(request.body)
        utype, user = user_type(request)
        if utype == 'error':
            return JsonResponse({'error': 'login'})
        if utype == 'user':
            return JsonResponse({'error': 'authority'})
        try:
            contest = Contest.objects.get(id=post['contestId'])
        except Contest.DoesNotExist:
            return JsonResponse({'error': 'contest not exist'})
        response = {}
        userStatus = {}
        userStatus['registered'] = 0
        try:
            participation = Participation.objects.get(targetContestId=contest.id,
                                                      userId=user.id)
            userStatus['registered'] = 1
            userStatus['verified'] = 0
            userStatus['submitted'] = 0
            if participation.checkStatus == 'accept':
                userStatus['verified'] = 1
            if participation.completeStatus == 'completed':
                response['relation'] = 'submitted'

        except Participation.DoesNotExist:
            pass
        return JsonResponse(response)
    return JsonResponse({'error': 'need POST method'})
