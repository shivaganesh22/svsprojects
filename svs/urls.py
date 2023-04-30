"""
URL configuration for svs project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from app.views import *
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
 #userpaths
    path('',home,name="home"),
    path('accounts/login/',signin,name="login"),
    path('signup',signup,name="signup"),
    path('logout',signout),
    path("videos",usrvideos),
    path("results",results),
    path("quizes",allquizes),
    path("video/<int:id>",player),
    path("video/reattempt/<int:id>",replayer),
    path("quiz/<int:vid>/<int:id>",take_quiz),

#adminpaths
    path("a",dashboard),
    #video
    path("a/videos",videos),
    path("a/videos/add",addvideos),
    path("a/video/edit/<int:id>",updatevideo),
    path("a/video/delete/<int:id>",deletevideo),
    path("a/video/<int:id>",adminplayer),

    #quiz
    path("a/quizes",quizes),
    path("a/quiz/add",addquiz),
    path("a/quiz/edit/",noquiz),
    path("a/quiz/edit/<int:id>",updatequiz),
    path("a/quiz/delete/<int:id>",deletequiz),
    path("a/quiz/result/<int:id>",exam_results),
    path("a/quiz/response/<int:id>",responses),

]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
