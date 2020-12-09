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
            try:
                contactUser = User.objects.get(id=post['currentContactId'])
            except User.DoesNotExist:
                return JsonResponse({'error': 'currentContactId not exist'})
            response['contact'].append({'id': contactUser.id,
                                        'username': contactUser.username,
                                        'avatar': contactUser.avatar,
                                        'newMessage': 0})
        for i in retrieved_dialog[start_pos: end_pos]:
            z = User.objects.get(id=i.sender)
            contact_ele = {'id': z.id, 'username': z.username,
                           'avatar': z.avatar, 'newMessage': 1 if i.updateTime > i.refreshTime else 0}
            response['contact'].append(contact_ele)
        return JsonResponse(response)
    return JsonResponse({'error': 'need POST method'})


def apiMessageCurrent(request):
    if request.method == 'POST':
        post = eval(request.body)
        utype, user = user_type(request)
        if utype == 'error':
            return JsonResponse({'error': 'login'})
        try:
            current_user = User.objects.get(id=post['currentContactId'])
        except User.DoesNotExist:
            return JsonResponse({'error': 'currentContactId not exist'})
        try:
            dialog = Dialog.objects.get(sender=current_user.id, receiver=user.id)
            dialog.refreshTime = time.mktime(datetime.datetime.now().timetuple())
            dialog.save()
        except Dialog.DoesNotExist:
            return JsonResponse({'currentMessage': []})
        message_send = Message.objects.filter(sender=user.id,
                                              receiver=current_user.id)
        print(message_send)
        message_receive = Message.objects.filter(sender=current_user.id,
                                                 receiver=user.id)
        message = message_receive | message_send
        message = message.order_by('sendTime')
        response = {'currentMessage': []}
        for i in range(min(len(message), 50)):
            response['currentMessage'].append({'sender': message[i].sender,
                                               'receiver': message[i].receiver,
                                               'content': message[i].content,
                                               'sendTime': message[i].sendTime})
        return JsonResponse(response)
    return JsonResponse({'error': 'need POST method'})


def apiMessageNew(request):
    if request.method == 'POST':
        post = eval(request.body)
        utype, user = user_type(request)
        if utype == 'error':
            return JsonResponse({'error': 'login'})
        try:
            current_user = User.objects.get(id=post['contactId'])
        except User.DoesNotExist:
            return JsonResponse({'error': 'contactId not exist'})
        now = time.mktime(datetime.datetime.now().timetuple())
        try:
            dialog1 = Dialog.objects.get(sender=current_user.id,
                                         receiver=user.id)
            dialog2 = Dialog.objects.get(sender=user.id,
                                         receiver=current_user.id)
            dialog1.updateTime = now
            dialog2.updateTime = now
            dialog1.refreshTime = now
        except Dialog.DoesNotExist:
            dialog1 = Dialog(sender=current_user.id, receiver=user.id,
                             updateTime=now, refreshTime=now)
            dialog2 = Dialog(sender=user.id, receiver=current_user.id,
                             updateTime=now, refreshTime=0)
        dialog1.save()
        dialog2.save()
        message = Message(sender=user.id, receiver=current_user.id,
                          content=post['content'], sendTime=now)
        message.save()
        return JsonResponse({'message': 'ok'})
    return JsonResponse({'error': 'need POST method'})
