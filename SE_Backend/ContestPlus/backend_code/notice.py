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

        # file_dir = str(settings.BASE_DIR) + "\\Images\\ContestHead\\"
        # file_name_parts = str(file.name).split('.')
        # file.name = str(picture_id) + '.' + file_name_parts[1]
        # url = host_prefix + "ContestHead/" + file.name
        # contest = Contest.objects.filter(id=content_id)
        # if len(contest) > 0:
        #     contest[0].thumb = url
        #     contest[0].save()
        # else:
        #     return JsonResponse({'error': 'Contest not found'})
        # new_picture = Picture(picture_id=picture_id, url=url, hostType=type, hostId=content_id)
        # new_picture.save()

        return_data = {}
        errorId = []

        return JsonResponse(return_data)
    return JsonResponse({'error': 'need POST method'})


def apiNoticeModify(request):
    return


def apiNoticeBrowse(request):
    return