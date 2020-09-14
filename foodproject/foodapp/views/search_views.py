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
# wikidocks필요해 b/c input == 고추 -> results of 청양고추, 고추, 꽈리고추 can output
# if split_my_input:
    # for i in split_my_input:
        # for menu in all_menu:
            # if Menu.objects.filter(name__contains=i):
                # current_menu = Menu.objects.filter(name__contains=i)
            # if len(list(current_menu.values_list)) == 1:


# 링크처리하는 부분 처리하기

def search(request):
    #1. 고기({메뉴:재료}), 면({메뉴:재료})
    input = request.GET.get('food')
    split_my_input = input.split(', ')

    meat_including_menus = ((Menu.objects.filter(Essential_Ingredient__contains='베이컨')|Menu.objects.filter(Essential_Ingredient__contains='다진 돼지고기')
    |Menu.objects.filter(Essential_Ingredient__contains='고기')|Menu.objects.filter(Essential_Ingredient__contains='소고기')
    |Menu.objects.filter(Essential_Ingredient__contains='목살')|Menu.objects.filter(Essential_Ingredient__contains='대패삼겹살')
    |Menu.objects.filter(Essential_Ingredient__contains='앞다리살')|Menu.objects.filter(Essential_Ingredient__contains='양념돼지갈비')
    |Menu.objects.filter(Essential_Ingredient__contains='닭다리살')))

    noodle_including_menus = ((Menu.objects.filter(Essential_Ingredient__contains='면')|Menu.objects.filter(Essential_Ingredient__contains='쫄면')
    |Menu.objects.filter(Essential_Ingredient__contains='라면')|Menu.objects.filter(Essential_Ingredient__contains='우동')
    |Menu.objects.filter(Essential_Ingredient__contains='칼국수')|Menu.objects.filter(Essential_Ingredient__contains='우동사리')))

    meat_food = {}
    for i in range(len(list(meat_including_menus.values_list('name',flat=True)))):
        meat_food[list(meat_including_menus.values_list('name',flat=True))[i]] = list(meat_including_menus.values_list('Essential_Ingredient',flat=True))[i]

    noodle_food = {}
    for ii in range(len(list(noodle_including_menus.values_list('name',flat=True)))):
        noodle_food[list(noodle_including_menus.values_list('name',flat=True))[ii]] = list(noodle_including_menus.values_list('Essential_Ingredient',flat=True))[ii]

    #2. 메뉴 범위 정하기
    menus = Menu.objects.all().order_by('name')
    names = menu_list = list(Menu.objects.order_by('name').values_list('name', flat=True))
    ingredients = ingredients_of_menu_list = list(Menu.objects.values_list('Essential_Ingredient', flat=True))
    #
    # if '고기' in input:
    #     menu_list = [iias for iias in menu_list if iias in list(meat_food.keys())]
    #     ingredients_of_menu_list = list(meat_food.values())
    #
    # if '면' in input:
    #     menu_list = [ias for ias in menu_list if ias in list(noodle_food.keys())]
    #     ingredients_of_menu_list = list(noodle_food.values())

    #3. 검색실행
    # category_menu = ['고기', '면']
    save_my_input = []
    menu_one, menu_two, menu_three, menu_four = {}, {}, {}, {}
    i = 0
    while (i < len(menu_list)):
        for input1 in split_my_input:
            q = 0
            while(q < len(ingredients_of_menu_list[i].split(', '))):
                if (ingredients_of_menu_list[i].split(', '))[q].startswith(' '):
                    (ingredients_of_menu_list[i].split(', '))[q] = ((ingredients_of_menu_list[i].split(', '))[q])[1:]
                #
                # if input1 in category_menu:
                #     break

                if input1 == (ingredients_of_menu_list[i].split(', '))[q]:
                    save_my_input.append(input1)

                q = q + 1
        #
        length_variable = len(save_my_input)
        # for q in category_menu:
        #     if q in split_my_input:
        #         length_variable = length_variable + 1

        if len(split_my_input) == length_variable:
            if len(ingredients_of_menu_list[i].split(', ')) == 1 and Menu.objects.values_list('link', flat=True).get(name=menu_list[i]):
                menu_one[menu_list[i]] = ingredients_of_menu_list[i]

            elif len(ingredients_of_menu_list[i].split(', ')) == 2 and Menu.objects.values_list('link', flat=True).get(name=menu_list[i]):
                menu_two[menu_list[i]] = ingredients_of_menu_list[i]

            elif len(ingredients_of_menu_list[i].split(', ')) == 3 and Menu.objects.values_list('link', flat=True).get(name=menu_list[i]):
                menu_three[menu_list[i]] = ingredients_of_menu_list[i]

            elif len(ingredients_of_menu_list[i].split(', ')) > 3 and Menu.objects.values_list('link', flat=True).get(name=menu_list[i]):
                menu_four[menu_list[i]] = ingredients_of_menu_list[i]

        save_my_input = []
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
    # obj = Menu.objects
    # menumenu = [menu for menu in menus]
    # namename = [menu.name for menu in menus]
    # ingreingre = [len(menu.Essential_Ingredient.split(', ')) for menu in menus]
    # linklink = [menu.link for menu in menus]

    context = {
    # 'obj':obj,'bbb':bbb,
    # 'menumenu':menumenu, 'tmp':tmp, 'tmp_queryset':tmp_queryset,'obj':obj,
    # 'namename':namename, 'ingreingre':ingreingre, 'linklink':linklink,
    'link_for_one': link_for_one, 'link_for_two': link_for_two, 'link_for_three':link_for_three, 'link_for_four':link_for_four,
    'menu_one_zipper':menu_one_zipper, 'menu_two_zipper':menu_two_zipper,'menu_three_zipper':menu_three_zipper,'menu_four_zipper':menu_four_zipper,
    'ingredients_of_menu_list':ingredients_of_menu_list, 'menu_list':menu_list,
    'ingredients' :ingredients, 'input' : input, 'menus' : menus, 'names':names,
    'menu_one' : menu_one, 'menu_two' : menu_two, 'menu_three' : menu_three, 'menu_four' : menu_four,
    }
    return render(request, 'foodapp/search.html', context)
