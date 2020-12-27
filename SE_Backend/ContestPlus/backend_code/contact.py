import datetime
from django.http import JsonResponse
from ContestPlus.backend_code.secure import *
from django.db.models import F


# 获取最新的聊天对象列表
def api_message_get(request):
    if request.method == 'POST':
        post = eval(request.body)
        us_type, user = user_type(request)
        if us_type == 'error':
            return JsonResponse({'error': 'login'})
        page_num = post['pageNum']
        page_size = post['pageSize']
        retrieved_dialog = Dialog.objects.filter(receiver=user.id)\
                                         .order_by('-updateTime')
        if post['type'] == 'Unread':
            retrieved_dialog = retrieved_dialog.filter(
                updateTime__gt=F('refreshTime'))
        if page_num <= 0 or page_size <= 0:
            start_pos = 0
            end_pos = len(retrieved_dialog)
        else:
            start_pos = (page_num - 1) * page_size
            end_pos = page_num * page_size
        response = {'contact': []}
        if post['currentContactId'] != -1:
            try:
                contact_user = User.objects.get(id=post['currentContactId'])
                response['contact'].append({'id': contact_user.id,
                                            'newMessage': 0,
                                            'username': contact_user.username,
                                            'avatar': contact_user.avatar})
            except User.DoesNotExist:
                if not post['currentContactId']:
                    response['contact'].append({'id': 0,
                                                'newMessage': 0,
                                                'username': '系统通知',
                                                'avatar': ''})
                else:
                    return JsonResponse({'error': 'currentContactId not exist'})
        for i in retrieved_dialog[start_pos: end_pos]:
            try:
                z = User.objects.get(id=i.sender)
                contact_ele = {'id': z.id, 'username': z.username,
                               'avatar': z.avatar,
                               'newMessage': 1 if(i.updateTime >
                                                  i.refreshTime) else 0}
                response['contact'].append(contact_ele)
            except User.DoesNotExist:
                if i.sender == 0:
                    contact_ele = {'id': 0, 'username': '系统通知',
                                   'avatar': '',
                                   'newMessage': 1 if (i.updateTime >
                                                       i.refreshTime) else 0}
                    response['contact'].append(contact_ele)
        return JsonResponse(response)
    return JsonResponse({'error': 'need POST method'})


# 获取当前聊天对象的聊天内容
def api_message_current(request):
    if request.method == 'POST':
        post = eval(request.body)
        us_type, user = user_type(request)
        if us_type == 'error':
            return JsonResponse({'error': 'login'})
        try:
            _ = User.objects.get(id=post['currentContactId'])
        except User.DoesNotExist:
            if post['currentContactId']:
                return JsonResponse({'error': 'currentContactId not exist'})
        try:
            dialog = Dialog.objects.get(sender=post['currentContactId'],
                                        receiver=user.id)
            dialog.refreshTime = time.mktime(datetime.datetime.now()
                                                     .timetuple())
            dialog.save()
        except Dialog.DoesNotExist:
            return JsonResponse({'currentMessage': []})
        message_send = Message.objects.filter(sender=user.id,
                                              receiver=post['currentContactId'])
        print(message_send)
        message_re = Message.objects.filter(sender=post['currentContactId'],
                                            receiver=user.id)
        message = message_re | message_send
        message = message.order_by('sendTime')
        response = {'currentMessage': []}
        for i in range(min(len(message), 50)):
            response['currentMessage'].append({'sender': message[i].sender,
                                               'receiver': message[i].receiver,
                                               'content': message[i].content,
                                               'sendTime': message[i].sendTime})
        return JsonResponse(response)
    return JsonResponse({'error': 'need POST method'})


# 发送一条新私信
def api_message_new(request):
    if request.method == 'POST':
        post = eval(request.body)
        us_type, user = user_type(request)
        if us_type == 'error':
            return JsonResponse({'error': 'login'})
        try:
            current_user = User.objects.get(id=post['contactId'])
        except User.DoesNotExist:
            return JsonResponse({'error': 'contactId not exist'})
        if user.id == current_user.id:
            return JsonResponse({'error': 'can not send message to yourself'})
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


# 系统发送私信
def send_system_message(message, user_id):
    user = User.objects.get(id=user_id)
    now = time.mktime(datetime.datetime.now().timetuple())
    try:
        dialog = Dialog.objects.get(sender=0, receiver=user.id)
        dialog.updateTime = now
    except Dialog.DoesNotExist:
        dialog = Dialog(sender=0, receiver=user.id, updateTime=now,
                        refreshTime=0)
    dialog.save()
    message = Message(sender=0, receiver=user.id,
                      content=message, sendTime=now)
    message.save()
