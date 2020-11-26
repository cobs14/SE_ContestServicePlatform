import random
import time
import datetime
import rsa
import hashlib
import requests
import json
import os
from django.http import JsonResponse
from django.conf import settings
from ContestPlus.backend_code.models import *
from ContestPlus.backend_code.secure import Jwt

false = False
true = True


def apiHandlePicReserve(request):
    if request.method == 'POST':
        try:
            request_body = eval(request.body)
            count = request_body.get('count')
        except:
            return JsonResponse({"error": "invalid parameters"})
        counter = Counter.objects.filter(name='picture_id')
        if len(counter) > 0:
            return_val = counter[0].value
            counter[0].value += count
            counter[0].save()
            response = {}
            picture_id = []
            for z in range(1, count + 1):
                return_val_counted = return_val + z
                picture_id.append(return_val_counted)
            response['pictureId'] = picture_id
            return JsonResponse(response)
        else:
            return JsonResponse({'error': 'counter lost'})
    return JsonResponse({'error': 'need POST method'})


def apiHandlePicUpload(request):
    if request.method == 'POST':
        try:
            info_raw = request.POST.get('config')
        except:
            return JsonResponse({"error": "invalid parameters"})
        config = json.loads(info_raw)
        print(config)
        return_data={}
        errorId=[]
        for z in config:
            try:
                picture_id = z['pictureId']
                type = z['type']
                content_id = z['contentId']
                file_key = z['fileKey']
            except:
                return JsonResponse({"error": "invalid parameters"})
            file = request.FILES.get(file_key, None)
            if not file:
                errorId.append(picture_id)
                continue
            file_dir=str(settings.BASE_DIR)+"\\Images\\Test\\"
            destination = open(os.path.join(file_dir, file.name), 'wb+')
            for chunk in file.chunks():
                destination.write(chunk)
            destination.close()

        return_data['errorId']=errorId
        return JsonResponse(return_data)
    return JsonResponse({'error': 'need POST method'})


def apiHandlePicDelete(request):
    if request.method == 'POST':
        try:
            request_body = eval(request.body)
            count = request_body.get('count')
        except:
            return JsonResponse({"error": "invalid parameters"})
    return JsonResponse({'error': 'need POST method'})


def apiHandlePicView(request):
    if request.method == 'POST':
        try:
            request_body = eval(request.body)
            count = request_body.get('count')
        except:
            return JsonResponse({"error": "invalid parameters"})
    return JsonResponse({'error': 'need POST method'})
# def upload_file(request):
#     if request.method == "POST":    # 请求方法为POST时，进行处理
#         myFile =request.FILES.get("myfile", None)    # 获取上传的文件，如果没有文件，则默认为None
#         if not myFile:
#             returnHttpResponse("no files for upload!")
#         destination = open(os.path.join("E:\\upload",myFile.name),'wb+')    # 打开特定的文件进行二进制的写操作
#         for chunk in myFile.chunks():      # 分块写入文件
#             destination.write(chunk)
#         destination.close()
#         returnHttpResponse("upload over!")
