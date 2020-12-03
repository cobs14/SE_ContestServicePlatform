import datetime
from django.http import JsonResponse
from ContestPlus.backend_code.secure import *
from django.db.models import F


def apiMessageContact(request):
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


def apiMessageGet(request):
    if request.method == 'POST':
        post = eval(request.body)
        utype, user = user_type(request)
        if utype == 'error':
            return JsonResponse({'error': 'login'})
        pageNum = post['pageNum']
        pageSize = post['pageSize']
        retrieved_dialog = Dialog.objects.filter(receiver=user.id).order_by('-updateTime')
        if post['type'] == 'Unread':
            retrieved_dialog = retrieved_dialog.filter(updateTime__gt=F('refreshTime'))
        if pageNum == 0 or pageSize == 0:
            start_pos = 0
            end_pos = len(retrieved_dialog)
        else:
            start_pos = (pageNum - 1) * pageSize
            end_pos = pageNum * pageSize
        response = {'contact': []}
        if post['currentContactId']:
            contactUser = User.objects.get(id=post['currentContactId'])
            response['contact'].append({'id': contactUser.id,
                                        'username': contactUser.username,
                                        'avatar': contactUser.avatar,
                                        'newMessage': 0})
        for z in retrieved_dialog[start_pos: end_pos]:
            contact_ele = {'id': z.id, 'username': z.username,
                           'avatar': z.avatar, 'newMessage': 0 if z.updateTime > z.refreshTime else 1}
            response['contact'].append(contact_ele)
        return JsonResponse(response)
    return JsonResponse({'error': 'need POST method'})


def apiMessageCurrent(request):
    if request.method == 'POST':
        post = eval(request.body)
        utype, user = user_type(request)
        if utype == 'error':
            return JsonResponse({'error': 'login'})
        current_user = User.objects.get(id=post['currentContactId'])
        message_send = Message.objects.filter(sender=user.id,
                                              receiver=current_user.id)
        message_receive = Message.objects.filter(sender=current_user.id,
                                                 receiver=user.id)
        message = message_receive | message_send
        message = message.order_by('-sendTime')
        if len(message) > 50:
            return JsonResponse({'currentMessage': message[: 50]})
        return JsonResponse({'currentMessage': message})
    return JsonResponse({'error': 'need POST method'})
