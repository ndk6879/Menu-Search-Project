from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from ..models import Menu
import sys
import io
import cgi
from django.urls import reverse
from ..forms import MenuForm

def search(request):

    #1. 메뉴 범위 정하기]
    menus = Menu.objects.all().order_by('name')
    names = menus.values_list('name', flat=True)
    ingredients = names.values_list('Essential_Ingredient', flat=True)

    input = request.GET.get('food')
    split_my_input = input.split(', ')

    if '고기' in input:
        names = menus.values_list('name', flat=True).filter(category__contains='고기')
        ingredients = names.values_list('Essential_Ingredient', flat=True)

    if '면' in input:
        names = menus.values_list('name', flat=True).filter(category__contains='면')
        ingredients = names.values_list('Essential_Ingredient', flat=True)

    if '채소' in input:
        names = menus.values_list('name', flat=True).filter(category__contains='채소')
        ingredients = names.values_list('Essential_Ingredient', flat=True)

    #2. 검색실행
    category_menu = ['고기', '면', '채소']
    menu_one, menu_two, menu_three, menu_four = [], [], [], []

    i = 0
    count = 0 #입력값과 재료가 같으면 +1
    while (i < len(names)):
        for input1 in split_my_input: #한 메뉴의 재료를 split_my_input이 훑음.
            if input1 in category_menu:
                count += 1
                continue

            q = 0
            while(q < len(ingredients[i].split(', '))):
                # if (ingredients_of_menu_list [i].split(', '))[q].startswith(' '):
                #     (ingredients_of_menu_list [i].split(', '))[q] = ((ingredients_of_menu_list [i].split(', '))[q])[1:]

                if input1 == (ingredients[i].split(', '))[q]:
                    count += 1

                q = q + 1

        if len(split_my_input) == count:
            if len(ingredients[i].split(', ')) == 1 and Menu.objects.values_list('link', flat=True).get(name=names[i]):
                menu_one.append(Menu.objects.get(name=names[i]))

            elif len(ingredients[i].split(', ')) == 2 and Menu.objects.values_list('link', flat=True).get(name=names[i]):
                menu_two.append(Menu.objects.get(name=names[i]))

            elif len(ingredients[i].split(', ')) == 3 and Menu.objects.values_list('link', flat=True).get(name=names[i]):
                menu_three.append(Menu.objects.get(name=names[i]))

            elif len(ingredients[i].split(', ')) > 3 and Menu.objects.values_list('link', flat=True).get(name=names[i]):
                menu_four.append(Menu.objects.get(name=names[i]))

        count = 0
        i = i + 1

    context = {
    'names':names, 'ingredients' :ingredients, 'input' : input, 'menus' : menus,
    'menu_one' : menu_one, 'menu_two' : menu_two, 'menu_three' : menu_three, 'menu_four' : menu_four,
    }
    return render(request, 'foodapp/search.html', context)
