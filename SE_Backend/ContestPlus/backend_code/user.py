import datetime
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
