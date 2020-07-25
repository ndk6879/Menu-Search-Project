from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Menu
import sys
import io
import cgi
from django.urls import reverse
from .forms import MenuForm



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
def test(request, food):
    menus = Menu.objects.all().order_by('name')
    food = Menu.objects.all().get(name=food)
    Essential_Ingredient = Menu.objects.values_list('Essential_Ingredient', flat=True).get(name=food) #모델에 있는 메뉴 재료
    Nonessential_Ingredient = Menu.objects.values_list('Nonessential_Ingredient', flat=True).get(name=food) #모델에 있는 메뉴 재료
    link = Menu.objects.values_list('link', flat=True).get(name=food) #모델에 있는 메뉴 재료
    tip = Menu.objects.values_list('tip', flat=True).get(name=food) #모델에 있는 메뉴 재료
    context = {'menus':menus, 'food' : food, 'Essential_Ingredient' : Essential_Ingredient, 'Nonessential_Ingredient':Nonessential_Ingredient,
    'link' : link, 'tip' : tip}
    return render(request, 'foodapp/test.html', context)

def index(request):
    menus = Menu.objects.all().order_by('name')
    names = (list(Menu.objects.values_list('name', flat=True))) #모델에 있는 메뉴 #flat을 사용하면 tuple말고 리스트 형태로 가져올 수 있다.
    ingredients = list(Menu.objects.values_list('Essential_Ingredient', flat=True)) #모델에 있는 메뉴 재료
    nonessential_ingredients = list(Menu.objects.values_list('Nonessential_Ingredient', flat=True)) #모델에 있는 메뉴 재료
    links = list(Menu.objects.values_list('link', flat=True)) #모델에 있는 메뉴 재료
    zippers = zip(names, links)
    context = {'menus':menus, 'names':names, 'links': links, 'zippers':zippers}
    return render(request, 'foodapp/index.html', context)

def search(request):
    menus = Menu.objects.all().order_by('name')
    names = list(Menu.objects.values_list('name', flat=True))
    ingredients = list(Menu.objects.values_list('Essential_Ingredient', flat=True))

    meat_including_menus = ((Menu.objects.filter(Essential_Ingredient__contains='베이컨')|Menu.objects.filter(Essential_Ingredient__contains='다진 돼지고기')
    |Menu.objects.filter(Essential_Ingredient__contains='고기')|Menu.objects.filter(Essential_Ingredient__contains='소고기')
    |Menu.objects.filter(Essential_Ingredient__contains='목살')|Menu.objects.filter(Essential_Ingredient__contains='대패삼겹살')
    |Menu.objects.filter(Essential_Ingredient__contains='앞다리살')|Menu.objects.filter(Essential_Ingredient__contains='양념돼지갈비')
    |Menu.objects.filter(Essential_Ingredient__contains='닭 다리살')))

    noodle_including_menus = ((Menu.objects.filter(Essential_Ingredient__contains='면')|Menu.objects.filter(Essential_Ingredient__contains='쫄면')
    |Menu.objects.filter(Essential_Ingredient__contains='라면')|Menu.objects.filter(Essential_Ingredient__contains='우동')
    |Menu.objects.filter(Essential_Ingredient__contains='칼국수')|Menu.objects.filter(Essential_Ingredient__contains='우동사리')))

    meat_including_menus_names = list(meat_including_menus.values_list('name',flat=True))
    meat_including_menus_ingredients = list(meat_including_menus.values_list('Essential_Ingredient',flat=True))
    noodle_including_menus_names = list(noodle_including_menus.values_list('name',flat=True))
    noodle_including_menus_ingredients = list(noodle_including_menus.values_list('Essential_Ingredient',flat=True))

    meat_food = {}
    for i in range(len(meat_including_menus_names)):
        meat_food[meat_including_menus_names[i]] = meat_including_menus_ingredients[i]

    noodle_food = {}
    for i in range(len(noodle_including_menus_names)):
        noodle_food[noodle_including_menus_names[i]] = noodle_including_menus_ingredients[i]

    menu_list = names
    ingredients_of_menu_list = ingredients
    category_menu = ['고기', '면']
    input = request.GET.get('food')
    split_my_input = input.split(', ')

    if '고기' in input:
        menu_list = [iias for iias in menu_list if iias in list(meat_food.keys())]
        ingredients_of_menu_list = list(meat_food.values())

    if '면' in input:
        menu_list = [ias for ias in menu_list if ias in list(noodle_food.keys())]
        ingredients_of_menu_list = [qdz for qdz in ingredients_of_menu_list if qdz in list(noodle_food.values())]

    save_my_input = []
    menu_one, menu_two, menu_three, menu_four = [], [], [], []
    menu_one_ingredient, menu_two_ingredient, menu_three_ingredient, menu_four_ingredient = [], [], [], []
    i = 0
    while (i < len(menu_list)):
        for input1 in split_my_input:
            q = 0
            while(q < len(ingredients_of_menu_list[i].split(', '))):
                if (ingredients_of_menu_list[i].split(', '))[q].startswith(' '):
                    (ingredients_of_menu_list[i].split(', '))[q] = ((ingredients_of_menu_list[i].split(', '))[q])[1:]

                if input1 in category_menu:
                    break

                if input1 == (ingredients_of_menu_list[i].split(', '))[q]:
                    save_my_input.append(input1)

                q = q + 1

        length_variable = len(save_my_input) #면, 마늘
        for q in category_menu: #고기, 면
            if q in split_my_input:
                length_variable = length_variable + 1

        if len(split_my_input) == length_variable:
            if len(ingredients_of_menu_list[i].split(', ')) == 1:
                menu_one.append(menu_list[i])
                menu_one_ingredient.append(ingredients_of_menu_list[i])

            elif len(ingredients_of_menu_list[i].split(', ')) == 2:
                menu_two.append(menu_list[i])
                menu_two_ingredient.append(ingredients_of_menu_list[i])

            elif len(ingredients_of_menu_list[i].split(', ')) == 3:
                menu_three.append(menu_list[i])
                menu_three_ingredient.append(ingredients_of_menu_list[i])

            elif len(ingredients_of_menu_list[i].split(', ')) > 3:
                menu_four.append((menu_list[i]))
                menu_four_ingredient.append(ingredients_of_menu_list[i])

        save_my_input = []
        i = i + 1

    menu_one_zipper = ''
    menu_two_zipper = ''
    menu_three_zipper = ''
    menu_four_zipper = ''
    links = list(Menu.objects.values_list('link', flat=True)) #모델에 있는 메뉴 재료

    link_for_one = [menu.link for menu in menus for x in menu_one if menu.name == x]
    link_for_two = [menu.link for menu in menus for x in menu_two if menu.name == x]
    link_for_three = [menu.link for menu in menus for x in menu_three if menu.name == x]
    link_for_four = [menu.link for menu in menus for x in menu_four if menu.name == x]

    if menu_one: menu_one_zipper = list(zip(menu_one, [x for x in menu_one_ingredient], link_for_one))
    if menu_two: menu_two_zipper = list(zip(menu_two, [x for x in menu_two_ingredient], link_for_two))
    if menu_three: menu_three_zipper = list(zip(menu_three, [x for x in menu_three_ingredient], link_for_three))
    if menu_four: menu_four_zipper = list(zip(menu_four, [x for x in menu_four_ingredient], link_for_four))

    context = {
    'menu_one_zipper':menu_one_zipper, 'menu_two_zipper':menu_two_zipper,'menu_three_zipper':menu_three_zipper,'menu_four_zipper':menu_four_zipper,
    'ingredients_of_menu_list':ingredients_of_menu_list, 'menu_list':menu_list,
    'ingredients' :ingredients, 'meat_including_menus_ingredients':meat_including_menus_ingredients,
    'names':names, 'meat_including_menus_names' : meat_including_menus_names, 'noodle_including_menus_names' : noodle_including_menus_names,
    'input' : input, 'menus' : menus, 'meat_including_menus' : meat_including_menus, 'noodle_including_menus_ingredients':noodle_including_menus_ingredients,
    'menu_one' : menu_one, 'menu_two' : menu_two, 'menu_three' : menu_three, 'menu_four' : menu_four,
    'menu_one_ingredient' : menu_one_ingredient, 'menu_two_ingredient' : menu_two_ingredient, 'menu_three_ingredient' : menu_three_ingredient, 'menu_four_ingredient' :menu_four_ingredient,
    }
    return render(request, 'foodapp/search.html', context)

def create(request):
    menus = Menu.objects.all().order_by('name')
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
