import json
import os
import platform
from django.http import JsonResponse
from django.http import FileResponse
from django.http import HttpResponse

from django.conf import settings
from ContestPlus.models import *
from ContestPlus.backend_code.secure import *

false = False
true = True


def checkPlatform(string):
    print(platform.system())
    if platform.system()=="Linux":
        string.replace("\\","/")
    return string


def apiSubmitUpload(request):
    if request.method == 'POST':
        try:
            contest_id = request.POST.get('contestId')
            participant_id = request.POST.get('participantId')
            file_key=request.POST.get('fileKey')
            if file_key != '':
                file = request.FILES.get(file_key, None)
        except:
            return JsonResponse({"error": "invalid parameters"})
        contest = Contest.objects.filter(id=contest_id)
        if contest[0].allowGroup == True:
            participation = Participation.objects.filter(targetContestId=contest_id, userId=participant_id)
            if len(participation) < 1:
                return JsonResponse({"error": "please apply"})
            group_id=participation[0].participantId
            extra_part = Participation.objects.filter(targetContestId=contest_id,participantId=group_id)
            participation=participation.union(extra_part)
        else:
            participation = Participation.objects.filter(targetContestId=contest_id, participantId=participant_id)
            if len(participation) < 1:
                return JsonResponse({"error": "please apply"})
        if file_key != '':
            file_dir = checkPlatform(str(settings.BASE_DIR) + "/files/needPermission/submission/" +
                                     contest_id + "/")
            if os.path.exists(file_dir) == False:
                os.makedirs(file_dir)
            # TODO: FIXME: 判断None好像还是必要的吧，毕竟空字符串和None还是不一样，貌似后端很多代码都只判断了是否为空串
            if participation[0].submissionDir != None and participation[0].submissionDir != '':
                old_file_name = participation[0].submissionDir.split('/')[-1]
                print(old_file_name)
                os.remove(os.path.join(file_dir, old_file_name))

            original_file_name=file.name
            file_name_parts = str(file.name).split('.')
            file.name = str(participation[0].participantId) + '.' + file_name_parts[-1]
            # host_prefix = 'http://127.0.0.1:8000/static/'

            for z in participation:
                z.submissionDir = file_dir + file.name
                z.submissionName = original_file_name
                z.save()

            destination = open(os.path.join(file_dir, file.name), 'wb+')
            for chunk in file.chunks():
                destination.write(chunk)
            destination.close()
        else:
            # TODO: FIXME: Bug fix (.name -> .submissionDir)
            if participation[0].submissionDir:
                os.remove(os.path.join(participation[0].submissionDir))
            for z in participation:
                z.submissionDir = ''
                z.submissionName = ''
                z.save()
        # TODO: FIXME: 后端应根据实际情况修改这部分代码，前端目前只保证其能够满足前端需要
        if file_key != '':
            participation[0].completeStatus = 'completed'
        else:
            participation[0].completeStatus = 'ready'
        participation[0].save()

        return JsonResponse({'message': 'ok'})
    return JsonResponse({'error': 'need POST method'})


def apiSubmitDownload(request):
    if request.method == 'POST':
        try:
            request_body = eval(request.body)
            contest_id = request_body['contestId']
            participant_id = request_body['participantId']
        except:
            return JsonResponse({"error": "invalid parameters"})
        contest = Contest.objects.filter(id=contest_id)
        participation = Participation.objects.filter(targetContestId=contest_id, userId=participant_id)

        if len(participation) < 1:
            return JsonResponse({"error": "please apply"})

        if participation[0].submissionDir=='':
            return JsonResponse({"error": "no submission"})
        else:
            response = HttpResponse(status=200)
            response['Content-Disposition'] = 'attachment; filename=%s' % participation[0].submissionName
            response['Content-Type'] = 'application/octet-stream'
            response['X-Accel-Redirect'] = '/file/submission/' + str(contest_id) + \
                                           '/' + str(participation[0].participantId) + \
                                           ".%s" % participation[0].submissionDir.split('.')[-1]
        return response
    return JsonResponse({'error': 'need POST method'})