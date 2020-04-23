from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Menu
import sys
import io
import cgi
from django.urls import reverse
from .forms import MenuForm

#nav var
# db구현화(name클릭하면 필드 나오기)
# essential재료, non-essneitals재료  & 양념들 어떻게 할지 -> model에서 non-essneitals재료 추가.
# 재료 입력 (고기 or 돼지고기)-> 동일검색결과
#views.refactoring
#search keywords by tag key
# # 나의 review & 댓글,후기, Q&A
# 배포

# 2가지 이상 재료 검색 & 검색창 설정하기 O
# url field만들기 O
# 없으면 출력 안시키기 O
# CSS 꾸미기 (index.page, create page) O
# db name 순서대로 OK


def index(request):
    menus = Menu.objects.all().order_by('name')
    names = Menu.objects.values_list('name', flat=True) #모델에 있는 메뉴
    ingredients = Menu.objects.values_list('Essential_Ingredient', flat=True) #모델에 있는 메뉴 재료

    new_dicts = {}
    for i in range(0, len(names)):
        new_dicts[names[i]] = ingredients[i]
    names_as_keys = list(new_dicts.keys())
    ingredients_as_values = list(new_dicts.values()) #new_dicts = {'마늘볶음밥' : '마늘, 밥, 버터', '국수' : '면, 육수'}

    ingredient_list = []
    for food in ingredients_as_values: # ingredients_as_values = '마늘, 밥, 버터', '국, 밥' , food = '마늘, 밥, 버터'
        if food:
            vv = food.split(',')
            ingredient_list.append(vv)         # ingredient_list = ['마늘', '밥', '버터'], [' 국', ' 밥']
        else:
            ingredient_list.append(food)         # ingredient_list = ['마늘', '밥', '버터'], [' 국', ' 밥']
    for ingredients in ingredient_list:
        i = 0
        new_list = []
        for ingredient in ingredients:
                if ingredient.startswith(' '):
                    s1 = ingredient[1:]
                    ingredients[i] = s1
                    if i == len(ingredients) - 1: #3
                        new_list.append(ingredients)
                    i += 1

                else:
                    s1 = ingredient
                    ingredients[i] = s1
                    if i == len(ingredients) - 1:
                        new_list.append(ingredients)
                    i += 1

    global dict_dict
    dict_dict = {}
    for q in range(0, len(names_as_keys)):
        dict_dict[names_as_keys[q]] = ingredient_list[q]    # dict_dict is the final and complete form of dictionary that we want.

    context = {'menus':menus}
    return render(request, 'foodapp/index.html', context)

def search(request):
    menus = Menu.objects.all()
    input = request.GET.get('practice_ingredient')
    split_my_input = input.split(', ') #밥, 마늘 -> ['밥', '마늘']
    save_my_input = []
    save_my_menu = []
    i = 0
    q = 0
    menu_one, menu_two, menu_three, menu_four = [], [], [], []
    menu_one_ingredient, menu_two_ingredient, menu_three_ingredient, menu_four_ingredient = [], [], [], []

    while (i < len(list(dict_dict.keys()))):
        for input in split_my_input:
            if input in ((list(dict_dict.values())[i])):
                save_my_input.append(input)
                if len(split_my_input) == len(save_my_input):
                    save_my_menu.append(list(dict_dict.keys())[i])
                    if len(list(dict_dict.values())[i]) == 1:
                        menu_one.append(list(dict_dict.keys())[i])
                        menu_one_ingredient.append(list(dict_dict.values())[i])

                    elif len(list(dict_dict.values())[i]) == 2:
                        menu_two.append(list(dict_dict.keys())[i])
                        menu_two_ingredient.append(list(dict_dict.values())[i])

                    elif len(list(dict_dict.values())[i]) == 3:
                        menu_three.append(list(dict_dict.keys())[i])
                        menu_three_ingredient.append(list(dict_dict.values())[i])

                    elif len(list(dict_dict.values())[i]) > 3:
                        menu_four.append(list(dict_dict.keys())[i])
                        menu_four_ingredient.append(list(dict_dict.values())[i])

        save_my_input = []
        i = i + 1

    len_try_a, len_try_b, len_try_c, len_try_d = len(menu_one), len(menu_two), len(menu_three), len(menu_four)

    menu_set1, menu_set2, menu_set3, menu_set4 = {}, {}, {}, {}
    try:
        for qq in range(0, len(menu_one)):
            menu_set1[menu_one[qq]] = ', '.join(menu_one_ingredient[qq])
    except:
        pass

    try:
        for qq in range(0, len(menu_two)):
            menu_set2[menu_two[qq]] = ', '.join(menu_two_ingredient[qq])
    except:
        pass

    try:
        for qq in range(0, len(menu_three)):
            menu_set3[menu_three[qq]] = ', '.join(menu_three_ingredient[qq])
    except:
        pass

    try:
        for qq in range(0, len(menu_four)):
            menu_set4[menu_four[qq]] = ', '.join(menu_four_ingredient[qq])
    except:
        pass

    context = {'input' : input, 'menus' : menus,
    'save_my_input' : save_my_input, 'save_my_menu' : save_my_menu,
    'menu_one' : menu_one, 'menu_two' : menu_two, 'menu_three' : menu_three, 'menu_four' : menu_four,
    'menu_one_ingredient' : menu_one_ingredient, 'menu_two_ingredient' : menu_two_ingredient, 'menu_three_ingredient' : menu_three_ingredient, 'menu_four_ingredient' :menu_four_ingredient,
    'menu_set1': menu_set1, 'menu_set2': menu_set2, 'menu_set3': menu_set3, 'menu_set4': menu_set4,
    'len_try_a' : len_try_a, 'len_try_b' : len_try_b, 'len_try_c' : len_try_c, 'len_try_d' : len_try_d
    }
    return render(request, 'foodapp/search.html', context)


def create(request):
    menus = Menu.objects.all()
    if request.method == 'POST':
        form = MenuForm(request.POST)
        if form.is_valid():
            obj = Menu(name=form.data['name'], Essential_Ingredient=form.data['Essential_Ingredient'], Nonessential_Ingredient=form.data['Nonessential_Ingredient'], link=form.data['link'], tip=form.data['tip'])
            obj.save()
            return redirect('http://127.0.0.1:8000/')
        return HttpResponse('fail')
    elif request.method == 'GET':
        form = MenuForm()
        return render(request, 'foodapp/form.html', {'form': form, 'menus' : menus})
    else:
        pass

    # menus = Menu.objects.all()
    # context = {'menus':menus}
    # if request.method == 'POST':
    #     return HttpResponse('Success')
    #     form = MenuForm(request.POST)
    #     if form.is_valid():
    #         obj = Menu(name=form.data['name'], Essential_Ingredient=form.data['Essential_Ingredient'], Nonessential_Ingredient=form.data['Nonessential_Ingredient'], link=form.data['link'], tip=form.data['tip'])
    #         obj.save()
    #         return HttpResponse('Success')
