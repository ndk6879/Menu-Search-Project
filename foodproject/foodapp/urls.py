from django.urls import path, re_path
from . import views
import sys
import io
import cgi
from .forms import *

app_name = 'foodapp'
urlpatterns = [
    path('', views.index, name = 'index'),
    path('form-test/', views.add_menu_button, name='form-test'),
    path('practice', views.search_menu_text, name = 'practice'),
]

#    re_path(r'^keword-parameter/(?P<cellphonee>010[1-9]\d{7})$', views.get_cellphone),

# def get_cellphone(request, cellphonee):
#     return HttpResponse("휴대폰번호는 {} 입니다.".format(cellphonee))


# - 재료 검색하면 검색한 걸 찾게 하기(파 -> 양파x)
# - 재료 전환시켜주는 거(대파, 파, 쪽파 -> 파)



# make_list = {}
# 1. menu의 key 값, value값을 받아서 묶어
# 2. 그리고 value에 ','가 있으면 그걸 한 묶음으로 나누기
# 3. 그리고 찾기!
#    get_menu = Menu.objects.all(field=menu)

#    menu_keys = list(Menu.keys())
#    menu_values = list(Menu.values())
#    for menu in menu_keys:
#        add.Menu(name)
#        save()
#
#    for ingredient in menu_values:
#        add.Menu(name)
#        save()
