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
from django.views.static import serve
from ContestPlus.backend_code import contest



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/register/info', views.apiRegister),
    path('api/register/verifymail', views.apiRegisterVerifyMail),
    path('api/contest/retrieve', views.apiContestRetrieve),
    path('api/key', views.apiKey),
    path('api/login', views.apiLogin),
    path('api/qualification', views.apiQualification),

    path('api/contest/creation', contest.apiContestCreation),
    path('api/contest/status', contest.apiContestStatus),
    path('api/contest/<int:contestId>/apply', contest.apiContestApply),
    path('api/contest/modify',contest.apiContestModify),


    path('api/handlepic/reserve', picture.apiHandlePicReserve),
    path('api/handlepic/upload', picture.apiHandlePicUpload),
    path('api/handlepic/delete', picture.apiHandlePicDelete),
    path('api/handlepic/view', picture.apiHandlePicView),
    path(r'^static/(?P<path>.*)$', serve, {'document_root': '/Statics/ '})
]
