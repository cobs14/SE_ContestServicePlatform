"""SE_Backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from ContestPlus.backend_code import account
from ContestPlus.backend_code import picture
from ContestPlus.backend_code import contest
from ContestPlus.backend_code import contact
from ContestPlus.backend_code import notice
from ContestPlus.backend_code import user
from ContestPlus.backend_code import submit
from ContestPlus.backend_code import grade
from ContestPlus.backend_code import certificate
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/register/info', account.apiRegister),
    path('api/register/verifymail', account.apiRegisterVerifyMail),
    path('api/reset', account.apiReset),
    path('api/reset/code', account.apiResetCode),
    path('api/reset/password', account.apiResetPassword),

    path('api/key', account.apiKey),
    path('api/login', account.apiLogin),
    path('api/qualification', account.apiQualification),
    path('api/qualification/manual',account.apiQualificationManual),
    path('api/qualification/fetch',account.apiQualificationFetch),
    path('api/qualification/file',account.apiQualificationFile),
    path('api/qualification/verify',account.apiQualificationVerify),
    path('api/code/generate', account.apiGenerateInvitationCode),
    path('api/code/browse', account.apiBrowseInvitationCode),

    path('api/contest/retrieve', contest.apiContestRetrieve),
    path('api/contest/creation', contest.api_contest_creation),
    path('api/contest/status', contest.api_contest_status),
    path('api/contest/modify',contest.apiContestModify),
    path('api/contest/apply', contest.api_contest_apply),
    path('api/contest/applystatus', contest.api_contest_apply_status),
    path('api/contest/list', contest.api_contest_list),

    path('api/handlepic/reserve', picture.apiHandlePicReserve),
    path('api/handlepic/upload', picture.apiHandlePicUpload),
    path('api/handlepic/delete', picture.apiHandlePicDelete),
    path('api/handlepic/view', picture.apiHandlePicView),

    path('api/message/currentmessage', contact.api_message_current),
    path('api/message/getmessage', contact.api_message_get),
    path('api/message/newmessage', contact.api_message_new),

    path('api/notice/new', notice.apiNoticeNew),
    path('api/notice/modify', notice.apiNoticeModify),
    path('api/notice/delete', notice.apiNoticeDelete),
    path('api/notice/browse', notice.apiNoticeBrowse),
    path('api/notice/download', notice.apiNoticeDownload),

    path('api/user', user.api_user),
    path('api/user/contact', user.api_user_contact),
    path('api/user/retrieve', user.api_user_retrieve),
    path('api/user/groupcode', user.api_user_group_code),
    path('api/user/checkrelation', user.api_user_check_relation),
    path('api/user/information', user.api_user_info),
    path('api/session', user.api_session),
    path('api/offline', user.api_offline),

    path('api/submit/upload', submit.apiSubmitUpload),
    path('api/submit/download', submit.apiSubmitDownload),
    path('api/submit/submissions', submit.apiSubmitSubmissions),

    path('api/grade/sheet', grade.api_grade_sheet),
    path('api/grade/download', grade.api_grade_download),
    path('api/grade/upload', grade.api_grade_upload),
    path('api/grade/submitsheet', grade.api_grade_submit_sheet),


    path('api/certification/get', certificate.apiCertificationGet),
    path('api/certification/getmy', certificate.apiCertificationGetMy),
    path('api/certification/award', certificate.apiCertificationAward),
    path('api/certification/verify', certificate.apiCertificationVerify)
    # path(r'^static/(?P<path>.*)$', serve, {'document_root': '/Statics/ '})

]
