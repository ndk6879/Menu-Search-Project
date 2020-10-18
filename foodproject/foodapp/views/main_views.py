# 재료 찾는 파트를 method로 만들어서 호출하기 -> 그 부분의 코드가 짧아지고 가독성이 높아지고 따로 관리하고 수정하기 편ㅡ안
# 공통되는 변수들을 묶어서 publicize해서 여러군데에서 사용하게 하기 -> 각각의 메소드(함수)에 다시 따로 만들 필요가 없음

# 검색할 때 split()설정.
# ETC part
# 해본 음식은 색깔 바꾸게 하기. -> JS
# search keywords by tag key

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from ..models import Menu
import sys
import io
import cgi
from django.urls import reverse
from ..forms import MenuForm


menus = Menu.objects.all().order_by('name') #모든데 다 쓰임
names = menus.values_list('name', flat=True)

def index(request):
    context = {'menus':menus, 'names':names}
    return render(request, 'foodapp/index.html', context)

def test(request, food):
    food = Menu.objects.get(name=food)

    context = {'menus':menus,
    'food':food,
    }
    return render(request, 'foodapp/test.html', context)

def create(request):
    if request.method == 'POST':
        form = MenuForm(request.POST)
        if form.is_valid():
            obj = Menu(name=form.data['name'], Essential_Ingredient=form.data['Essential_Ingredient'], Nonessential_Ingredient=form.data['Nonessential_Ingredient'], link=form.data['link'], tip=form.data['tip'])
            obj.save()
            return redirect('http://127.0.0.1:8000/')
        return HttpResponse('fail')
    elif request.method == 'GET':
        form = MenuForm()
        return render(request, 'foodapp/create.html', {'form': form, 'menus' : menus})
    else:
        pass
