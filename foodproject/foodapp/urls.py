from django.urls import path, re_path
from django.conf.urls import url
from . import views
import sys
import io
import cgi
from .forms import *

app_name = 'foodapp'
urlpatterns = [
    path('', views.index, name = 'index'),
    path('create', views.create, name='create'),
    path('search', views.search, name = 'search'),
    path('test/<str:food>', views.test, name = 'test'),
    # re_path(r'^test/(?P<food>[\w\s]+)$',views.test, name = 'test'),
    # re_path(r'^testing/(?P<testing>.+)$',views.testing, name = 'testing')
]

#    re_path(r'^keword-parameter/(?P<cellphonee>010[1-9]\d{7})$', views.get_cellphone),

# def get_cellphone(request, cellphonee):
#     return HttpResponse("휴대폰번호는 {} 입니다.".format(cellphonee))
