import datetime
from django.http import JsonResponse
from ContestPlus.backend_code.secure import *


def apiContestStatus(request):
    if request.method == 'POST':
        post = eval(request.body)
        utype, _ = user_type(request)
        if utype != 'admin':
            return JsonResponse({'error': 'login'})
        try:
            contest = Contest.objects.get(id=post['id'])
            if contest.censorStatus != 'Pending':
                return JsonResponse({'error': 'status'})
        except:
            return JsonResponse({'error': 'contest'})
        if post['status']:
            contest.censorStatus = 'Accept'
        else:
            contest.censorStatus = 'Reject'
        contest.save()
        return JsonResponse({'message': 'ok'})
    return JsonResponse({'error': 'need POST method'})


def apiContestApply(request, contestId):
    if request.method == 'POST':
        post = eval(request.body)
        utype, user = user_type(request)
        if utype != 'user':
            return JsonResponse({'error': 'login'})
        try:
            contest = Contest.objects.get(id=contestId)
            if contest.censorStatus != 'Accept':
                return JsonResponse({'error': 'status'})
            now_time = time.mktime(datetime.datetime.now().timetuple())
            un_time = time.mktime(contest.applyStartTime.timetuple())
            un_time2 = time.mktime(contest.applyDeadline.timetuple())
            if not (un_time <= now_time <= un_time2):
                return JsonResponse({'error': 'applyTime'})
        except Contest.DoesNotExist:
            return JsonResponse({'error': 'contest'})
        if not contest.allowGroup:
            participation = Participation(participantId=user.id,
                                          targetContestId=contestId)
        else:
            member = str(post['participantId'][0])
            for i in post['participantId'][1:]:
                member += ',' + str(i)
            group = Group(name=post['groupName'],
                          description=post['description'],
                          memberCount=len(post['participantId']),
                          memberId=member)
            group.save()
            participation = Participation(participantId=group.id,
                                          targetContestId=contestId)
        participation.save()
        return JsonResponse({'message': 'ok'})
    return JsonResponse({'error': 'need POST method'})


def apiContestCreation(request):
    if request.method == 'POST':
        post = eval(request.body)
        utype, user = user_type(request)
        if utype == 'error':
            return JsonResponse({'error': 'login'})
        if utype != 'sponsor':
            return JsonResponse({'error': 'authority'})
        contest = Contest(title=post['title'], module=post['module'],
                          description=post['description'],
                          allowGroup=post['allowGroup'], sponsorId=user.id,
                          applyStartTime=post['applyStartTime'],
                          applyDeadline=post['applyDeadline'],
                          contestStartTime=post['contestStartTime'],
                          contestDeadline=post['contestDeadline'],
                          censorStatus=False, abstract=post['abstract'],
                          reviewStartTime=post['reviewStartTime'],
                          reviewDeadline=post['reviewDeadline'])
        if post['allowGroup']:
            contest.maxGroupMember = post['maxGroupMember']
            contest.minGroupMember = post['minGroupMember']
        contest.save()
        return JsonResponse({'message': 'ok', 'id': contest.id})
    return JsonResponse({'error': 'need POST method'})


def apiContestModify(request):
    if request.method == 'POST':
        post = eval(request.body)
        contest_id = post['contestId']
        modify_attribute = post['modifyAttribute']
        modify_value = post['modifyValue']

        utype, user = user_type(request)
        if utype == 'error':
            return JsonResponse({'error': 'login'})
        if utype != 'sponsor':
            return JsonResponse({'error': 'authority'})
        contest = Contest.objects.filter(id=contest_id)
        if len(contest) > 0:
            target_contest=contest[0]
            if modify_attribute == 'title':
                target_contest.title = modify_value
            elif modify_attribute == 'module':
                target_contest.module = modify_value
            elif modify_attribute == 'abstract':
                target_contest.abstract = modify_value
            elif modify_attribute == 'description':
                target_contest.description = modify_value
            elif modify_attribute == 'allowGroup':
                target_contest.allowGroup = modify_value
            elif modify_attribute == 'applyStartTime':
                target_contest.applyStartTime = modify_value
            elif modify_attribute == 'applyDeadline':
                target_contest.applyDeadline = modify_value
            elif modify_attribute == 'contestStartTime':
                target_contest.contestStartTime = modify_value
            elif modify_attribute == 'contestDeadline':
                target_contest.contestDeadline = modify_value
            elif modify_attribute == 'reviewStartTime':
                target_contest.reviewStartTime = modify_value
            elif modify_attribute == 'reviewDeadline':
                target_contest.reviewDeadline = modify_value
            elif modify_attribute == 'minGroupMember':
                target_contest.minGroupMember = modify_value
            elif modify_attribute == 'maxGroupMember':
                target_contest.maxGroupMember = modify_value
            else:
                return JsonResponse({'error': 'attribute invalid'})
            target_contest.save()
        else:
            return JsonResponse({'error': 'contest not found'})
        return JsonResponse({'message': 'ok', 'id': contest.id})
    return JsonResponse({'error': 'need POST method'})


def apiContestRetrieve(request):
    if request.method == 'POST':
        try:
            request_body = eval(request.body)
            params = request_body.get('params')
            pageNum = request_body.get('pageNum')
            pageSize = request_body.get('pageSize')
        except:
            return JsonResponse({"error": "invalid parameters"})
        retrieved_contest = Contest.objects.all()

        contest_id = params['id']
        if contest_id != 0:
            retrieved_contest = retrieved_contest.filter(id=contest_id)
        sponsor_id = params['sponsorId']
        if sponsor_id != 0:
            retrieved_contest = retrieved_contest.filter(sponsorId=sponsor_id)

        allow_group = params['allowGroup']
        if allow_group != "Any":
            if allow_group == 'True':
                retrieved_contest = retrieved_contest.filter(allowGroup=True)
            if allow_group == 'False':
                retrieved_contest = retrieved_contest.filter(allowGroup=False)

        censorStatus = params['censorStatus']
        if censorStatus != "Any":
            if censorStatus == 'Pending':
                usertype, _ = user_type(request)
                if usertype != 'admin':
                    return JsonResponse({'error': 'authority'})
                retrieved_contest = retrieved_contest.filter(censorStatus='pending')
            if censorStatus == 'Accept':
                retrieved_contest = retrieved_contest.filter(censorStatus='accept')
            if censorStatus == 'Reject':
                usertype, _ = user_type(request)
                if usertype != 'admin':
                    return JsonResponse({'error': 'authority'})
                retrieved_contest = retrieved_contest.filter(censorStatus='reject')

        module = params['module']
        if len(module) > 0:
            module_retrieved_contest = Contest.objects.none()
            for z in module:
                module_retrieved_step = retrieved_contest.filter(module__contains=z)
                module_retrieved_contest = module_retrieved_contest | module_retrieved_step
            retrieved_contest = module_retrieved_contest

        text = params['text']
        if len(text) > 0:
            title_text_retrieved_contest = Contest.objects.none()
            for z in text:
                title_text_retrieved_step = retrieved_contest.filter(title__contains=z)
                title_text_retrieved_contest = title_text_retrieved_contest.union(title_text_retrieved_step)

            abstract_text_retrieved_contest = Contest.objects.none()
            for z in text:
                abstract_text_retrieved_step = retrieved_contest.filter(abstract__contains=z)
                abstract_text_retrieved_contest = abstract_text_retrieved_contest.union(abstract_text_retrieved_step)

            description_text_retrieved_contest = Contest.objects.none()
            for z in text:
                description_text_retrieved_step = retrieved_contest.filter(description__contains=z)
                description_text_retrieved_contest = description_text_retrieved_contest.union \
                    (description_text_retrieved_step)
            retrieved_contest = title_text_retrieved_contest.union \
                (abstract_text_retrieved_contest, description_text_retrieved_contest)

        state = params['state']
        apply = state['apply']
        contest = state['contest']
        review = state['review']

        now_time = datetime.datetime.now()
        un_time_now = time.mktime(now_time.timetuple())

        if apply != 0:
            if apply == 1:
                beforeApply = Contest.objects.none()
                for z in retrieved_contest:
                    if un_time_now < z.applyStartTime:
                        beforeApply = beforeApply.union(Contest.objects.filter(id=z.id))
                retrieved_contest = beforeApply

            if apply == 2:
                duringApply = Contest.objects.none()
                for z in retrieved_contest:
                    if z.applyDeadline > un_time_now > z.applyStartTime:
                        duringApply = duringApply.union(Contest.objects.filter(id=z.id))
                retrieved_contest = duringApply

            if apply == 3:
                afterApply = Contest.objects.none()
                for z in retrieved_contest:
                    if z.applyDeadline < un_time_now:
                        afterApply = afterApply.union(Contest.objects.filter(id=z.id))
                retrieved_contest = afterApply

        if contest != 0:
            if contest == 1:
                beforeContest = Contest.objects.none()
                for z in retrieved_contest:
                    if un_time_now < z.contestStartTime:
                        beforeContest = beforeContest.union(Contest.objects.filter(id=z.id))
                retrieved_contest = beforeContest

            if contest == 2:
                duringContest = Contest.objects.none()
                for z in retrieved_contest:
                    if z.contestDeadline > un_time_now > z.contestStartTime:
                        duringContest = duringContest.union(Contest.objects.filter(id=z.id))
                retrieved_contest = duringContest

            if contest == 3:
                afterContest = Contest.objects.none()
                for z in retrieved_contest:
                    if un_time_now > z.contestDeadline:
                        afterContest = afterContest.union(Contest.objects.filter(id=z.id))
                retrieved_contest = afterContest

        if review != 0:
            if review == 1:
                beforeReview = Contest.objects.none()
                for z in retrieved_contest:
                    if un_time_now < z.reviewStartTime:
                        beforeReview = beforeReview.union(Contest.objects.filter(id=z.id))
                retrieved_contest = beforeReview

            if review == 2:
                duringReview = Contest.objects.none()
                for z in retrieved_contest:
                    if z.reviewDeadline > un_time_now > z.reviewStartTime:
                        duringReview = duringReview.union(Contest.objects.filter(id=z.id))
                retrieved_contest = duringReview

            if review == 3:
                afterReview = Contest.objects.none()
                for z in retrieved_contest:
                    if un_time_now > z.reviewDeadline:
                        afterReview = afterReview.union(Contest.objects.filter(id=z.id))
                retrieved_contest = afterReview

        if pageNum == 0 or pageSize == 0:
            start_pos = 0
            end_pos = len(retrieved_contest)
        else:
            start_pos = (pageNum - 1) * pageSize
            end_pos = pageNum * pageSize
        response = {}
        response['count'] = retrieved_contest.count()
        response_contest = []
        for z in retrieved_contest[start_pos:end_pos]:
            response_contest_ele = {}
            response_contest_ele['id'] = z.id
            response_contest_ele['title'] = z.title
            sponsor = User.objects.filter(id=z.sponsorId)
            if len(sponsor) > 0:
                response_contest_ele['sponsor'] = sponsor[0].username
            else:
                response_contest_ele['sponsor'] = ''
            response_contest_ele['abstract'] = z.abstract
            response_contest_ele['module'] = z.module
            state = {}
            state['apply'] = [z.applyStartTime, z.applyDeadline]
            state['contest'] = [z.contestStartTime, z.contestDeadline]
            state['review'] = [z.reviewStartTime, z.reviewDeadline]
            response_contest_ele['state'] = state
            response_contest_ele['allowGroup'] = z.allowGroup
            response_contest_ele['imgUrl'] = z.thumb
            detailed = params['detailed']
            if detailed == True:
                response_contest_ele['description'] = z.description
            response_contest.append(response_contest_ele)

        response['data'] = response_contest
        return JsonResponse(response)
    return JsonResponse({'error': 'need POST method'})