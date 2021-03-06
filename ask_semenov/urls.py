"""ask_semenov URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from blog import views as blogViews

urlpatterns = [
    url(r'^admin/', admin.site.urls),
	url(r'^$', blogViews.mainPage, name="mainPage"),
	url(r'^hot/$', blogViews.hotQuestions, name="hotQuestions"),
	url(r'^tag/(?P<tag>\w+)/$', blogViews.taggedQuestions, name="taggedQuestions"),
	url(r'^question/(?P<questionID>\d+)/$', blogViews.answer, name="answer"),
	url(r'^login/$', blogViews.siteLogin, name="login"),
	url(r'^signup/$', blogViews.signup, name="signup"),
	url(r'^ask/$', blogViews.ask, name="askQuestion"),
	url(r'^edit/$', blogViews.settings, name="settings" ),
	url(r'^logout/$', blogViews.siteLogout, name="logout" ),
	url(r'^votes/$', blogViews.votes, name="votes" ),
	url(r'^correct/$', blogViews.correct, name="correct" ),
]
