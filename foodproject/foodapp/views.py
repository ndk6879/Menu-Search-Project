from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Menu
import sys
import io
import cgi
from django.urls import reverse
from .forms import MenuForm

# nav var PP
# db구현화(name클릭하면 필드 나오기) PP
# 양념들 어떻게 할지 -> model에서 non-essneitals재료 추가.PP
# 재료 입력 (고기 or 돼지고기)-> 동일검색결과 OK
# views.refactoring
# search keywords by tag key
# 나의 review & 댓글,후기, Q&A
# 배포

# 2가지 이상 재료 검색 & 검색창 설정하기 O
# url field만들기 O
# 없으면 출력 안시키기 O
# CSS 꾸미기 (index.page, create page) O
# db name 순서대로 OK

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
    names = Menu.objects.values_list('name', flat=True) #모델에 있는 메뉴
    ingredients = Menu.objects.values_list('Essential_Ingredient', flat=True) #모델에 있는 메뉴 재료

    new_dicts = {}
    for i in range(0, len(names)):
        new_dicts[names[i]] = ingredients[i]
    names_as_keys = list(new_dicts.keys())
    global ingredients_as_values
    ingredients_as_values = list(new_dicts.values()) #new_dicts = {'마늘볶음밥' : '마늘, 밥, 버터', '국수' : '면, 육수'}

    ingredient_list = []
    for food in ingredients_as_values: # ingredients_as_values = '마늘, 밥, 버터', '국, 밥' , food = '마늘, 밥, 버터'
        if food:
            vv = food.split(',')
            ingredient_list.append(vv)         # ingredient_list = ['마늘', '밥', '버터'], [' 국', ' 밥']
        else:
            ingredient_list.append(food)         # ingredient_list = ['마늘', '밥', '버터'], [' 국', ' 밥']

    for asd in ingredient_list:
        i = 0
        new_list = []
        for ingredient in asd:
                if ingredient.startswith(' '):
                    s1 = ingredient[1:]
                    asd[i] = s1
                    if i == len(asd) - 1: #3
                        new_list.append(asd)
                    i += 1

                else:
                    s1 = ingredient
                    asd[i] = s1
                    if i == len(asd) - 1:
                        new_list.append(asd)
                    i += 1

    global dict_dict
    dict_dict = {}
    for q in range(0, len(names_as_keys)):
        dict_dict[names_as_keys[q]] = ingredient_list[q]    # dict_dict is the final and complete form of dictionary that we want.

    context = {'menus':menus, 'names': names, 'ingredients':ingredients, 'ingredients_as_values':ingredients_as_values}
    return render(request, 'foodapp/index.html', context)

def search(request):
    menus = Menu.objects.all().order_by('name')
    meat_including_menus = (Menu.objects.filter(Essential_Ingredient__contains='베이컨')|Menu.objects.filter(Essential_Ingredient__contains='다진 돼지고기')|Menu.objects.filter(Essential_Ingredient__contains='소고기')|Menu.objects.filter(Essential_Ingredient__contains='목살')|Menu.objects.filter(Essential_Ingredient__contains='대패삼겹살')|Menu.objects.filter(Essential_Ingredient__contains='고기')|Menu.objects.filter(Essential_Ingredient__contains='닭 다리살'))

    meat_including_menus_names = meat_including_menus.values_list('name',flat=True)
    meat_including_menus_ingredients = meat_including_menus.values_list('Essential_Ingredient',flat=True)
    meat_including_menus_names_list = list(meat_including_menus_names)
    meat_including_menus_ingredients_list = list(meat_including_menus_ingredients)

    input = request.GET.get('practice_ingredient')
    split_my_input = input.split(', ') #밥, 마늘 -> ['밥', '마늘']
    save_my_input = []
    save_my_menu = []
    available_menu = ""
    available_menu_ingredienet = ""
    i = 0

    menu_one, menu_two, menu_three, menu_four = [], [], [], []
    menu_one_ingredient, menu_two_ingredient, menu_three_ingredient, menu_four_ingredient = [], [], [], []

    menu_list = ''
    ingredients_of_menu_list = ''

    if '고기' not in input:
        menu_list = list(dict_dict.keys())
        ingredients_of_menu_list = ingredients_as_values #list(dict_dict.values())

    elif '고기' in input:
        menu_list = meat_including_menus_names_list
        ingredients_of_menu_list = meat_including_menus_ingredients_list

    while (i < len(menu_list)):
        if '고기' not in split_my_input:
            for input1 in split_my_input:
                if input1 in ((ingredients_of_menu_list[i])):
                    save_my_input.append(input)

                    if len(split_my_input) == len(save_my_input):
                        save_my_menu.append(menu_list[i])
                        available_menu += (menu_list[i]) + ', '
                        available_menu_ingredienet += (ingredients_of_menu_list[i]) + ', '

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
                            menu_four.append(menu_list[i])
                            menu_four_ingredient.append(ingredients_of_menu_list[i])
            save_my_input = []
            i = i + 1

        elif '고기' in split_my_input:
            for input2 in split_my_input:
                if len(split_my_input) > 1 and input2 == '고기':
                    continue

                elif len(split_my_input) == 1 and input2 == '고기':
                    save_my_input.append(input2)
                    save_my_menu.append(menu_list[i])

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
                        menu_four.append(menu_list[i])
                        menu_four_ingredient.append(ingredients_of_menu_list[i])

                elif len(split_my_input) > 1 and input2 in ((ingredients_of_menu_list[i])):
                    save_my_input.append(input2)
                    if len(split_my_input) > 1 and len(split_my_input) - 1 == len(save_my_input):
                        save_my_menu.append(menu_list[i])
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
                            menu_four.append(menu_list[i])
                            menu_four_ingredient.append(ingredients_of_menu_list[i])
            save_my_input = []
            i = i + 1

            #     elif len(split_my_input) > 1 and input in ((ingredients_of_menu_list[i])):
            #         save_my_input.append(input2)
            #         if len(split_my_input) > 1 and len(split_my_input) - 1 == len(save_my_input):
            #             save_my_menu.append(menu_list[i])
            #             available_menu += (menu_list[i]) + ', '
            #             available_menu_ingredienet += (ingredients_of_menu_list[i]) + ', '
            #
            #             if len(ingredients_of_menu_list[i].split(', ')) == 1:
            #                 menu_one.append(menu_list[i])
            #                 menu_one_ingredient.append(ingredients_of_menu_list[i])
            #
            #             elif len(ingredients_of_menu_list[i].split(', ')) == 2:
            #                 menu_two.append(menu_list[i])
            #                 menu_two_ingredient.append(ingredients_of_menu_list[i])
            #
            #             elif len(ingredients_of_menu_list[i].split(', ')) == 3:
            #                 menu_three.append(menu_list[i])
            #                 menu_three_ingredient.append(ingredients_of_menu_list[i])
            #
            #             elif len(ingredients_of_menu_list[i].split(', ')) > 3:
            #                 menu_four.append(menu_list[i])
            #                 menu_four_ingredient.append(ingredients_of_menu_list[i])
            # save_my_input = []
            # i = i + 1

    len_try_a, len_try_b, len_try_c, len_try_d = len(menu_one), len(menu_two), len(menu_three), len(menu_four)

    menu_set1, menu_set2, menu_set3, menu_set4 = {}, {}, {}, {}

    if menu_one:
        for qq in range(0, len(menu_one)):
            menu_set1[menu_one[qq]] = (menu_one_ingredient[qq])

    if menu_two:
        for qq in range(0, len(menu_two)):
            menu_set2[menu_two[qq]] = (menu_two_ingredient[qq])


    if menu_three:
        for qq in range(0, len(menu_three)):
            menu_set3[menu_three[qq]] = (menu_three_ingredient[qq])

    if menu_four:
        for qq in range(0, len(menu_four)):
            menu_set4[menu_four[qq]] = (menu_four_ingredient[qq])


    context = {
    'input' : input, 'menus' : menus, 'meat_including_menus' : meat_including_menus,
    'available_menu' : available_menu, 'available_menu_ingredienet':available_menu_ingredienet,
    'menu_one' : menu_one, 'menu_two' : menu_two, 'menu_three' : menu_three, 'menu_four' : menu_four,
    'menu_one_ingredient' : menu_one_ingredient, 'menu_two_ingredient' : menu_two_ingredient, 'menu_three_ingredient' : menu_three_ingredient, 'menu_four_ingredient' :menu_four_ingredient,
    'menu_set1': menu_set1, 'menu_set2': menu_set2, 'menu_set3': menu_set3, 'menu_set4': menu_set4,
    'len_try_a' : len_try_a, 'len_try_b' : len_try_b, 'len_try_c' : len_try_c, 'len_try_d' : len_try_d
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
