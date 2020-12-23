import os
import zipfile
from django.http import JsonResponse
from django.http import HttpResponse

from django.conf import settings
from ContestPlus.backend_code.secure import *

false = False
true = True


def apiSubmitUpload(request):
    if request.method == 'POST':
        try:
            contest_id = request.POST.get('contestId')
            participant_id = request.POST.get('participantId')
            file_key = request.POST.get('fileKey')
            if file_key != '':
                file = request.FILES.get(file_key, None)
        except:
            return JsonResponse({"error": "invalid parameters"})
        contest = Contest.objects.filter(id=contest_id)
        if contest[0].allowGroup:
            participation = Participation.objects.filter(targetContestId=contest_id, userId=participant_id)
            if len(participation) < 1:
                return JsonResponse({"error": "please apply"})
            group_id = participation[0].participantId
            extra_part = Participation.objects.filter(targetContestId=contest_id, participantId=group_id)
            participation = participation.union(extra_part)
        else:
            participation = Participation.objects.filter(targetContestId=contest_id, participantId=participant_id)
            if len(participation) < 1:
                return JsonResponse({"error": "please apply"})
        if file_key != '':
            file_dir = checkPlatform(str(settings.BASE_DIR) + "/files/needPermission/submission/" +
                                     contest_id + "/")
            if not os.path.exists(file_dir):
                os.makedirs(file_dir)
            if participation[0].submissionDir is not None and participation[0].submissionDir != '':
                old_file_name = participation[0].submissionDir.split('/')[-1]
                os.remove(os.path.join(file_dir, old_file_name))

            original_file_name = file.name
            file_name_parts = str(file.name).split('.')
            file.name = str(participation[0].participantId) + '.' + file_name_parts[-1]
            # host_prefix = 'http://127.0.0.1:8000/static/'

            for z in participation:
                z.submissionDir = file_dir + file.name
                z.submissionName = original_file_name

            destination = open(os.path.join(file_dir, file.name), 'wb+')
            for chunk in file.chunks():
                destination.write(chunk)
            destination.close()
        else:
            if participation[0].submissionDir:
                os.remove(os.path.join(participation[0].submissionDir))
            for z in participation:
                z.submissionDir = ''
                z.submissionName = ''
        if file_key != '':
            for z in participation:
                z.completeStatus = 'completed'
        else:
            for z in participation:
                z.completeStatus = 'ready'
        for z in participation:
            z.save()

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

        if participation[0].submissionDir == '':
            return JsonResponse({"error": "no submission"})
        else:
            response = HttpResponse(status=200)
            response['Content-Disposition'] = 'attachment; filename=%s' % str(participation[0].participantId) + \
                                              ".%s" % participation[0].submissionDir.split('.')[-1]
            response['Content-Type'] = 'application/octet-stream'
            response['X-Accel-Redirect'] = '/file/submission/' + str(contest_id) + \
                                           '/' + str(participation[0].participantId) + \
                                           ".%s" % participation[0].submissionDir.split('.')[-1]
        return response
    return JsonResponse({'error': 'need POST method'})


def apiSubmitSubmissions(request):
    if request.method == 'POST':
        try:
            request_body = eval(request.body)
            contest_id = request_body['contestId']
            count=request_body['count']
            if count >= 0:
                participants=request_body['participantId']
        except:
            return JsonResponse({"error": "invalid parameters"})
        # contest = Contest.objects.filter(id=contest_id)
        submission_dir = checkPlatform(str(settings.BASE_DIR) + "/files/needPermission/submission/" +
                                       str(contest_id) + "/")

        zip_file_name = str(contest_id) + ".zip"

        if os.path.exists(submission_dir + zip_file_name):
            os.remove(os.path.join(submission_dir, zip_file_name))
        files_to_zip = os.listdir(submission_dir)

        zip_file = zipfile.ZipFile(submission_dir + zip_file_name, "w", zipfile.ZIP_DEFLATED)

        for z in files_to_zip:
            file_name = submission_dir + str(z)
            file_name_check=int(str(z).split(".")[0])
            if file_name_check in participants:
                participantion=Participation.objects.filter(participantId=file_name_check)
                if len(participantion)>0:
                    if participantion[0].type == 'single':
                        user = User.objects.filter(id=participantion[0].userId)
                        file_name_to_download=participantion[0].submissionName+'_'+user[0].trueName+'_id_' + str(z)
                    elif participantion[0].type == 'group':
                        group = Group.objects.filter(id=participantion[0].participantId)
                        file_name_to_download = participantion[0].submissionName+'_'+group[0].name+'_id_' + str(z)
                zip_file.write(file_name, "submissions/" + file_name_to_download)

        zip_file.close()

        response = HttpResponse(status=200)
        response['Content-Disposition'] = 'attachment; filename=%s' % str(contest_id) + \
                                          ".zip"
        response['Content-Type'] = 'application/octet-stream'
        response['X-Accel-Redirect'] = '/file/submission/' + str(contest_id) + \
                                       '/' + str(contest_id) + ".zip"
        return response
    return JsonResponse({'error': 'need POST method'})
