from django.urls import path, re_path
from django.conf.urls import url
from .views import main_views, search_views
import sys
import io
import cgi
from .forms import *

app_name = 'foodapp'
urlpatterns = [
    path('', main_views.index, name = 'index'),
    path('create', main_views.create, name='create'), #원래는 views.create(views.py에 있는 create함수)였는데 지금은 main_views.py에 있는 create함수
    path('search', search_views.search, name = 'search'),
    path('test/<str:food>', main_views.test, name = 'test'),
]
