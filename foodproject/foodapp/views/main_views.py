# 재료 찾는 파트를 method로 만들어서 호출하기 -> 그 부분의 코드가 짧아지고 가독성이 높아지고 따로 관리하고 수정하기 편ㅡ안
# 공통되는 변수들을 묶어서 publicize해서 여러군데에서 사용하게 하기 -> 각각의 메소드(함수)에 다시 따로 만들 필요가 없음

# 검색할 때 split()설정.
# ETC part
# 해본 음식은 색깔 바꾸게 하기. -> JS
# search keywords by tag key
# 모든 메뉴(All menu), 집밥 메뉴(home cook), 분위기 메뉴(Mood), 올킬 메뉴(Clearance)
# 배포

# 재료 입력 (고기 or 돼지고기)-> 동일검색결과. +면도 되게 하기. OK
# views.refactoring *띄어쓰기 상관없이 같은결과. OK
# db구현화(name클릭하면 필드 나오기) OK
# 나의 review & 댓글,후기, Q&A OK
# 이름 오류 바꾸기 OK
# 2가지 이상 재료 검색 & 검색창 설정하기 OK
# url field만들기 OK
# 없으면 출력 안시키기 OK
# CSS 꾸미기 (index.page, create page) OK
# db name 순서대로 OL

# nav var PP
# 양념들 어떻게 할지 -> model에서 non-essneitals재료 추가.PP

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from ..models import Menu
import sys
import io
import cgi
from django.urls import reverse
from ..forms import MenuForm


menus = Menu.objects.all().order_by('name') #모든데 다 쓰임
names = list(Menu.objects.values_list('name', flat=True))
#모델에 있는 메뉴 #flat을 사용하면 tuple말고 리스트 형태의 쿼리셋으로 가져올 수 있다.
#마지막에 list를 써서 쿼리셋을 리스트로 변환

def index(request):
    links = list(Menu.objects.values_list('link', flat=True))
    zippers = zip(names, links)
    context = {'menus':menus, 'names':names, 'links': links, 'zippers':zippers}
    return render(request, 'foodapp/index.html', context)

def test(request, food):
    food = Menu.objects.all().get(name=food)
    Essential_Ingredient = Menu.objects.values_list('Essential_Ingredient', flat=True).get(name=food)
    Nonessential_Ingredient = Menu.objects.values_list('Nonessential_Ingredient', flat=True).get(name=food)
    link = Menu.objects.values_list('link', flat=True).get(name=food)
    tip = Menu.objects.values_list('tip', flat=True).get(name=food)
    context = {'menus':menus, 'food' : food, 'Essential_Ingredient' : Essential_Ingredient, 'Nonessential_Ingredient':Nonessential_Ingredient,
    'link' : link, 'tip' : tip, 'names':names}
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
