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
from ContestPlus.backend_code import views
from ContestPlus.backend_code import picture
from ContestPlus.backend_code import contest
from ContestPlus.backend_code import contact
from ContestPlus.backend_code import notice
from ContestPlus.backend_code import user
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/register/info', views.apiRegister),
    path('api/register/verifymail', views.apiRegisterVerifyMail),

    path('api/key', views.apiKey),
    path('api/login', views.apiLogin),
    path('api/qualification', views.apiQualification),
    path('api/code/generate', views.apiGenerateInvitationCode),
    path('api/code/browse', views.apiBrowseInvitationCode),

    path('api/contest/retrieve', contest.apiContestRetrieve),
    path('api/contest/creation', contest.apiContestCreation),
    path('api/contest/status', contest.apiContestStatus),
    path('api/contest/modify',contest.apiContestModify),
    path('api/contest/apply', contest.apiContestApply),
    path('api/contest/applystatus', contest.apiContestApplyStatus),

    path('api/handlepic/reserve', picture.apiHandlePicReserve),
    path('api/handlepic/upload', picture.apiHandlePicUpload),
    path('api/handlepic/delete', picture.apiHandlePicDelete),
    path('api/handlepic/view', picture.apiHandlePicView),

    path('api/message/currentmessage', contact.apiMessageCurrent),
    path('api/message/getmessage', contact.apiMessageGet),
    path('api/message/newmessage', contact.apiMessageNew),

    path('api/notice/new', notice.apiNoticeNew),
    path('api/notice/modify', notice.apiNoticeModify),
    path('api/notice/delete', notice.apiNoticeDelete),
    path('api/notice/browse', notice.apiNoticeBrowse),
    path('api/notice/download', notice.apiNoticeDownload),

    path('api/user', user.apiUser),
    path('api/user/contact', user.apiUserContact),
    path('api/user/retrieve', user.apiUserRetrieve),
    path('api/user/checkrelation', user.apiUserCheckRelation),

    path(r'^static/(?P<path>.*)$', serve, {'document_root': '/Statics/ '})
]
