from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from ..models import Menu
import sys
import io
import cgi
from django.urls import reverse
from ..forms import MenuForm

#1. 메뉴 찾는 부분 윗부분(category_menu잇는 부분) 보기좋게 refactoring
#2. 음식, 재료 dictionary로 묶을 수 있지 않나?
#3. 링크처리하는 부분 처리하기

# wikidocs처럼. input == 고추 -> results of 청양고추, 고추, 꽈리고추 can output
# if split_my_input:
    # for i in split_my_input:
        # for menu in all_menu:
            # if Menu.objects.filter(name__contains=i):
                # current_menu = Menu.objects.filter(name__contains=i)
            # if len(list(current_menu.values_list)) == 1:

def search(request):
    #1. 고기, 면
    meat_including_menus = ((Menu.objects.filter(name__contains='고기')|Menu.objects.filter(Essential_Ingredient__contains='베이컨')|Menu.objects.filter(Essential_Ingredient__contains='다진 돼지고기')
    |Menu.objects.filter(Essential_Ingredient__contains='고기')|Menu.objects.filter(Essential_Ingredient__contains='소고기')
    |Menu.objects.filter(Essential_Ingredient__contains='목살')|Menu.objects.filter(Essential_Ingredient__contains='대패삼겹살')
    |Menu.objects.filter(Essential_Ingredient__contains='앞다리살')|Menu.objects.filter(Essential_Ingredient__contains='양념돼지갈비')
    |Menu.objects.filter(Essential_Ingredient__contains='닭다리살')))     #type =쿼리셋

    noodle_including_menus = (((Menu.objects.filter(name__contains='면')|Menu.objects.filter(Essential_Ingredient__contains='면')|Menu.objects.filter(Essential_Ingredient__contains='쫄면')
    |Menu.objects.filter(Essential_Ingredient__contains='라면')|Menu.objects.filter(Essential_Ingredient__contains='우동')
    |Menu.objects.filter(Essential_Ingredient__contains='칼국수')|Menu.objects.filter(Essential_Ingredient__contains='우동사리'))))

    #2. 메뉴 범위 정하기
    menus = Menu.objects.all().order_by('name')
    names = menus.values_list('name', flat=True)
    ingredients = names.values_list('Essential_Ingredient', flat=True)

    input = request.GET.get('food')
    split_my_input = input.split(', ')

    if '고기' in input:
        # ingredients  = names.values_list('Essential_Ingredient', flat=True)
        names = menus.values_list('name', flat=True).filter(category__contains='고기')
        ingredients = names.values_list('Essential_Ingredient', flat=True)
        # names = meat_including_menus.values_list('name', flat=True)
        # ingredients  = meat_including_menus.values_list('Essential_Ingredient', flat=True)

    if '면' in input:
        names = menus.values_list('name', flat=True).filter(category__contains='면')
        ingredients = names.values_list('Essential_Ingredient', flat=True)

    #3. 검색실행
    category_menu = ['고기', '면']
    menu_one, menu_two, menu_three, menu_four = {}, {}, {}, {}

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
                menu_one[names[i]] = ingredients[i]

            elif len(ingredients[i].split(', ')) == 2 and Menu.objects.values_list('link', flat=True).get(name=names[i]):
                menu_two[names[i]] = ingredients[i]

            elif len(ingredients[i].split(', ')) == 3 and Menu.objects.values_list('link', flat=True).get(name=names[i]):
                menu_three[names[i]] = ingredients[i]

            elif len(ingredients[i].split(', ')) > 3 and Menu.objects.values_list('link', flat=True).get(name=names[i]):
                menu_four[names[i]] = ingredients[i]

        count = 0
        i = i + 1

    #4. 링크처리
    link_for_one = [menu.link for x in (menu_one) for menu in menus if x == menu.name and menu.link and menu.link != '']
    link_for_two = [menu.link for x in (menu_two) for menu in menus if x == menu.name and menu.link and menu.link != '']
    link_for_three = [menu.link for x in (menu_three) for menu in menus if x == menu.name and menu.link and menu.link != '']
    link_for_four = [menu.link for x in (menu_four) for menu in menus if x == menu.name and menu.link and menu.link != '']

    menu_one_zipper = list(zip(menu_one, menu_one.values(), link_for_one))
    menu_two_zipper = list(zip(menu_two, menu_two.values(), link_for_two))
    menu_three_zipper = list(zip(menu_three, menu_three.values(), link_for_three))
    menu_four_zipper = list(zip(menu_four, menu_four.values(), link_for_four))
    #5.
    # Menu.objects.filter(Essential_Ingredient__contains='고기')
    # menus = Menu.objects.all().order_by('name')
    #
    # if split_my_input:
    #     for i in split_my_input:
    #         tmp = list(Menu.objects.values_list('name',flat=True).filter(name__contains=i))
    #         tmp_queryset = (Menu.objects.filter(name__contains=i))
    #         for ele in tmp_queryset:
    #             if len(ele.Essential_Ingredient.split(', ')) == 1:
    #                 menu_one[ele.name] = ele.Essential_Ingredient
    #             elif len(ele.Essential_Ingredient.split(', ')) == 2:
    #                 menu_two[ele.name] = ele.Essential_Ingredient
    #             elif len(ele.Essential_Ingredient.split(', ')) == 3:
    #                 menu_three[ele.name] = ele.Essential_Ingredient
    #             elif len(ele.Essential_Ingredient.split(', ')) > 3:
    #                 menu_four[ele.name] = ele.Essential_Ingredient

    context = {
    'link_for_one': link_for_one, 'link_for_two': link_for_two, 'link_for_three':link_for_three, 'link_for_four':link_for_four,
    'menu_one_zipper':menu_one_zipper, 'menu_two_zipper':menu_two_zipper,'menu_three_zipper':menu_three_zipper,'menu_four_zipper':menu_four_zipper,
    'ingredients':ingredients, 'names':names,
    'ingredients' :ingredients, 'input' : input, 'menus' : menus,
    'menu_one' : menu_one, 'menu_two' : menu_two, 'menu_three' : menu_three, 'menu_four' : menu_four,
    }
    return render(request, 'foodapp/search.html', context)
