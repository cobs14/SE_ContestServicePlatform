import json
import os
from django.http import JsonResponse
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
            file = request.FILES.get(file_key, None)
        except:
            return JsonResponse({"error": "invalid parameters"})
        new_notice=Notice(contest_id=contest_id,title=title,content=content,link=link,file='')
        new_notice.save()
        file_dir = str(settings.BASE_DIR) + "\\Files\\ContestNotice\\" + str(contest_id) + "\\"
        if os.path.exists(file_dir) == False:
            os.makedirs(file_dir)

        file_name_parts = str(file.name).split('.')
        file.name = str(new_notice.id) + '.' + file_name_parts[1]
        host_prefix = 'http://127.0.0.1:8000/static/'
        url = host_prefix + "Files/ContestNotice/" + str(contest_id) +"/"+ file.name
        new_notice.file=url
        new_notice.save()

        destination = open(os.path.join(file_dir, file.name), 'wb+')
        for chunk in file.chunks():
            destination.write(chunk)
        destination.close()

        return JsonResponse({'message':'ok'})
    return JsonResponse({'error': 'need POST method'})


def apiNoticeModify(request):
    return


def apiNoticeBrowse(request):
    return