import json
import os
from django.http import JsonResponse
from django.http import FileResponse
from django.conf import settings
from ContestPlus.models import *
from ContestPlus.backend_code.secure import *

false = False
true = True


def apiNoticeNew(request):
    if request.method == 'POST':
        try:
            contest_id = request.POST.get('contestId')
            title = request.POST.get('title')
            content = request.POST.get('content')
            link = request.POST.get('link')
            file_key = request.POST.get('fileKey')
            if file_key !='':
                file = request.FILES.get(file_key, None)
        except:
            return JsonResponse({"error": "invalid parameters"})

        # utype, user = user_type(request)
        # target_contest = Contest.objects.filter(id=contest_id)
        # if len(target_contest) < 1:
        #     return JsonResponse({"error": "contest not exist"})
        # if utype != 'sponsor' and utype != 'admin' and user.id != target_contest[0].sponsorId:
        #     return JsonResponse({"error": "permission denied"})

        new_notice = Notice(contest_id=contest_id, title=title, content=content, link=link, file='')

        new_notice.save()
        if file_key != '':
            file_dir = str(settings.BASE_DIR) + "\\Files\\ContestNotice\\" + str(contest_id) + "\\"
            if os.path.exists(file_dir) == False:
                os.makedirs(file_dir)

            file_name_parts = str(file.name).split('.')
            file.name = str(new_notice.id) + '.' + file_name_parts[-1]

            new_notice.file = file_dir+file.name
            new_notice.save()

            destination = open(os.path.join(file_dir, file.name), 'wb+')
            for chunk in file.chunks():
                destination.write(chunk)
            destination.close()

        return JsonResponse({'message': 'ok'})
    return JsonResponse({'error': 'need POST method'})


def apiNoticeModify(request):
    if request.method == 'POST':
        try:
            notice_id = request.POST.get('noticeId')
            title = request.POST.get('title')
            content = request.POST.get('content')
            link = request.POST.get('link')
            modified_file=request.POST.get('modifiedFile')
            if modified_file:
                file_key = request.POST.get('fileKey')
                if file_key !='':
                    file = request.FILES.get(file_key, None)
        except:
            return JsonResponse({"error": "invalid parameters"})

        notice = Notice.objects.filter(id=notice_id)
        if len(notice) < 1:
            return JsonResponse({"error": "notice not found"})
        notice[0].title = title
        notice[0].content = content
        notice[0].link = link

        # utype, user = user_type(request)
        # target_contest = Contest.objects.filter(id=notice[0].contest_id)
        # if len(target_contest) < 1:
        #     return JsonResponse({"error": "contest not exist"})
        # if utype != 'sponsor' and utype != 'admin' and user.id != target_contest[0].sponsorId:
        #     return JsonResponse({"error": "permission denied"})

        if modified_file:
            if file_key != '':
                file_dir = str(settings.BASE_DIR) + "\\Files\\ContestNotice\\" + str(notice[0].contest_id) + "\\"
                if os.path.exists(file_dir) == False:
                    os.makedirs(file_dir)
                if notice[0].file !='':
                    old_file_name = notice[0].file.split('\\')[-1]
                    os.remove(os.path.join(file_dir, old_file_name))

                file_name_parts = str(file.name).split('.')
                file.name = str(notice[0].id) + '.' + file_name_parts[-1]
                host_prefix = 'http://127.0.0.1:8000/static/'

                notice[0].file = file_dir+file.name

                destination = open(os.path.join(file_dir, file.name), 'wb+')
                for chunk in file.chunks():
                    destination.write(chunk)
                destination.close()
            else:
                if notice[0].file:
                    os.remove(os.path.join(notice[0].file))
                notice[0].file=''
        notice[0].save()
        return JsonResponse({'message': 'ok'})
    return JsonResponse({'error': 'need POST method'})


def apiNoticeDelete(request):
    if request.method == 'POST':
        try:
            request_body = eval(request.body)
            notice_id = request_body['noticeId']
        except:
            return JsonResponse({"error": "invalid parameters"})

        notice = Notice.objects.filter(id=notice_id)
        if len(notice) < 1:
            return JsonResponse({"error": "notice not found"})

        # utype, user = user_type(request)
        # target_contest = Contest.objects.filter(id=notice[0].contest_id)
        # if len(target_contest) < 1:
        #     return JsonResponse({"error": "contest not exist"})
        # if utype != 'sponsor' and utype != 'admin' and user.id != target_contest[0].sponsorId:
        #     return JsonResponse({"error": "permission denied"})

        if notice[0].file !='':
            file_dir = str(settings.BASE_DIR) + "\\Files\\ContestNotice\\" + str(notice[0].contest_id) + "\\"
            if os.path.exists(file_dir) == False:
                os.makedirs(file_dir)

            old_file_name = notice[0].file.split('\\')[-1]
            os.remove(os.path.join(file_dir, old_file_name))

        notice[0].delete()

        return JsonResponse({'message': 'ok'})
    return JsonResponse({'error': 'need POST method'})


def apiNoticeBrowse(request):
    if request.method == 'POST':
        try:
            request_body = eval(request.body)
            contest_id = request_body['contestId']
        except:
            return JsonResponse({"error": "invalid parameters"})

        notice = Notice.objects.filter(contest_id=contest_id)

        utype, user = user_type(request)

        return_data = {}
        return_data_notice_list = []
        for z in notice:
            return_data_notice_ele = {}
            if z.participantOnly and utype!='sponsor' and utype!='admin':
                return_data_notice_ele['error'] = 'need apply'
                return_data_notice_list.append(return_data_notice_ele)
                continue
            return_data_notice_ele['noticeId'] = z.id
            return_data_notice_ele['title'] = z.title
            return_data_notice_ele['content'] = z.content
            return_data_notice_ele['link'] = z.link
            if z.file != '':
                return_data_notice_ele['hasFile'] = 1
            else:
                return_data_notice_ele['hasFile'] = 0
            return_data_notice_list.append(return_data_notice_ele)
        return_data['count'] = len(return_data_notice_list)
        return_data['data'] = return_data_notice_list
        return JsonResponse(return_data)
    return JsonResponse({'error': 'need POST method'})


def apiNoticeDownload(request):
    if request.method == 'POST':
        try:
            request_body = eval(request.body)
            notice_id = request_body['noticeId']
        except:
            return JsonResponse({"error": "invalid parameters"})
        notice=Notice.objects.filter(id=notice_id)
        if len(notice) < 1:
            return JsonResponse({'error': 'Notice not found'})
        file_to_download=open(notice[0].file,"rb")
        response=FileResponse(file_to_download)
        response['content_type'] = "application/octet-stream"
        response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(notice[0].file)
        return response
    return JsonResponse({'error': 'need POST method'})
