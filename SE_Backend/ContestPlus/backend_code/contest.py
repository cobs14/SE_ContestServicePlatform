import datetime
from django.http import JsonResponse
from ContestPlus.backend_code.secure import *


def apiContestStatus(request):
    if request.method == 'POST':
        post = eval(request.body)
        utype, _ = user_type(request)
        if utype == 'error':
            return JsonResponse({'error': 'login'})
        if utype != 'admin':
            return JsonResponse({'error': 'authority'})
        try:
            contest = Contest.objects.get(id=post['id'])
            if contest.censorStatus != 'pending':
                return JsonResponse({'error': 'status'})
        except:
            return JsonResponse({'error': 'contest'})
        contest.censorString = post['message']
        if post['status']:
            contest.censorStatus = 'accept'
        else:
            contest.censorStatus = 'reject'
        contest.save()
        return JsonResponse({'message': 'ok'})
    return JsonResponse({'error': 'need POST method'})


def apiContestApply(request, contestId):
    if request.method == 'POST':
        post = eval(request.body)
        utype, user = user_type(request)
        if utype == 'error':
            return JsonResponse({'error': 'login'})
        if utype != 'user':
            return JsonResponse({'error': 'login'})
        try:
            contest = Contest.objects.get(id=contestId)
            if contest.censorStatus != 'accept':
                return JsonResponse({'error': 'status'})
            now_time = time.mktime(datetime.datetime.now().timetuple())
            if not (contest.applyStartTime <= now_time <= contest.applyDeadline):
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
                          censorStatus='pending', abstract=post['abstract'],
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
        try:
            contest_id = post.get('contestId')
            modify_attribute = post.get('modifyAttribute')
            modify_value = post.get('modifyValue')
        except:
            return JsonResponse({'error': 'invalid parameter'})
        utype, user = user_type(request)
        if utype == 'error':
            return JsonResponse({'error': 'login'})
        if utype != 'sponsor':
            return JsonResponse({'error': 'authority'})
        contest = Contest.objects.filter(id=contest_id)
        if len(contest) > 0:
            target_contest=contest[0]
            for z in range(0,len(modify_attribute)):
                if modify_attribute[z] == 'title':
                    target_contest.title = modify_value[z]
                elif modify_attribute[z] == 'module':
                    target_contest.module = modify_value[z]
                elif modify_attribute[z] == 'abstract':
                    target_contest.abstract = modify_value[z]
                elif modify_attribute[z] == 'description':
                    target_contest.description = modify_value[z]
                elif modify_attribute[z] == 'allowGroup':
                    target_contest.allowGroup = modify_value[z]
                elif modify_attribute[z] == 'applyStartTime':
                    target_contest.applyStartTime = modify_value[z]
                elif modify_attribute[z] == 'applyDeadline':
                    target_contest.applyDeadline = modify_value[z]
                elif modify_attribute[z] == 'contestStartTime':
                    target_contest.contestStartTime = modify_value[z]
                elif modify_attribute[z] == 'contestDeadline':
                    target_contest.contestDeadline = modify_value[z]
                elif modify_attribute[z] == 'reviewStartTime':
                    target_contest.reviewStartTime = modify_value[z]
                elif modify_attribute[z] == 'reviewDeadline':
                    target_contest.reviewDeadline = modify_value[z]
                elif modify_attribute[z] == 'minGroupMember':
                    target_contest.minGroupMember = modify_value[z]
                elif modify_attribute[z] == 'maxGroupMember':
                    target_contest.maxGroupMember = modify_value[z]
                else:
                    return JsonResponse({'error': 'attribute invalid'})
            target_contest.save()
        else:
            return JsonResponse({'error': 'contest not found'})
        return JsonResponse({'message': 'ok', 'id': target_contest.id})
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
        usertype, user_info = user_type(request)
        contest_id = params['id']
        if contest_id != 0:
            retrieved_contest = retrieved_contest.filter(id=contest_id)

        sponsor_id = params['sponsorId']
        if usertype == 'sponsor':
            sponsor_id = user_info.id
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
                if usertype == 'admin':
                    return JsonResponse({'error': 'authority'})
                retrieved_contest = retrieved_contest.filter(censorStatus='pending')
            if censorStatus == 'Accept':
                retrieved_contest = retrieved_contest.filter(censorStatus='accept')
            if censorStatus == 'Reject':
                if usertype != 'admin':
                    return JsonResponse({'error': 'authority'})
                retrieved_contest = retrieved_contest.filter(censorStatus='reject')
        else:
            if usertype == 'user':
                retrieved_contest = retrieved_contest.filter(censorStatus='accept')

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

        apply_retrieve = Contest.objects.none()
        contest_retrieve = Contest.objects.none()
        review_retrieve = Contest.objects.none()
        time_retrieve=Contest.objects.none()

        if apply != 0:
            if apply == 1:
                beforeApply = Contest.objects.none()
                for z in retrieved_contest:
                    if un_time_now < z.applyStartTime:
                        beforeApply = beforeApply.union(Contest.objects.filter(id=z.id))
                apply_retrieve = beforeApply

            if apply == 2:
                duringApply = Contest.objects.none()
                for z in retrieved_contest:
                    if z.applyDeadline > un_time_now > z.applyStartTime:
                        duringApply = duringApply.union(Contest.objects.filter(id=z.id))
                apply_retrieve = duringApply

            if apply == 3:
                afterApply = Contest.objects.none()
                for z in retrieved_contest:
                    if z.applyDeadline < un_time_now:
                        afterApply = afterApply.union(Contest.objects.filter(id=z.id))
                apply_retrieve = afterApply
            time_retrieve=time_retrieve.union(apply_retrieve)

        if contest != 0:
            if contest == 1:
                beforeContest = Contest.objects.none()
                for z in retrieved_contest:
                    if un_time_now < z.contestStartTime:
                        beforeContest = beforeContest.union(Contest.objects.filter(id=z.id))
                contest_retrieve = beforeContest

            if contest == 2:
                duringContest = Contest.objects.none()
                for z in retrieved_contest:
                    if z.contestDeadline > un_time_now > z.contestStartTime:
                        duringContest = duringContest.union(Contest.objects.filter(id=z.id))
                contest_retrieve = duringContest

            if contest == 3:
                afterContest = Contest.objects.none()
                for z in retrieved_contest:
                    if un_time_now > z.contestDeadline:
                        afterContest = afterContest.union(Contest.objects.filter(id=z.id))
                contest_retrieve = afterContest
            time_retrieve=time_retrieve.union(contest_retrieve)

        if review != 0:
            if review == 1:
                beforeReview = Contest.objects.none()
                for z in retrieved_contest:
                    if un_time_now < z.reviewStartTime:
                        beforeReview = beforeReview.union(Contest.objects.filter(id=z.id))
                review_retrieve = beforeReview

            if review == 2:
                duringReview = Contest.objects.none()
                for z in retrieved_contest:
                    if z.reviewDeadline > un_time_now > z.reviewStartTime:
                        duringReview = duringReview.union(Contest.objects.filter(id=z.id))
                review_retrieve = duringReview

            if review == 3:
                afterReview = Contest.objects.none()
                for z in retrieved_contest:
                    if un_time_now > z.reviewDeadline:
                        afterReview = afterReview.union(Contest.objects.filter(id=z.id))
                review_retrieve = afterReview
            time_retrieve=time_retrieve.union(review_retrieve)

        if review != 0 or contest != 0 or apply !=0:
            retrieved_contest=time_retrieve

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
                response_contest_ele['sponsorEmail'] = sponsor[0].email
            else:
                response_contest_ele['sponsor'] = ''
            response_contest_ele['abstract'] = z.abstract
            response_contest_ele['module'] = z.module
            response_contest_ele['censorStatus'] = z.censorStatus
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
        response_contest.reverse()
        response['data'] = response_contest
        return JsonResponse(response)
    return JsonResponse({'error': 'need POST method'})
