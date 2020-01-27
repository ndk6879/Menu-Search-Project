from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Menu
import sys
import io
import cgi
from django.urls import reverse
from .forms import MenuForm

# 2가지 이상 재료 검색 & 검색창 설정하기
# CSS 꾸미기
# 배포
# 재료 입력 (고기 or 돼지고기)-> 동일검색결과
# 양념들 어떻게 할지
# 댓글 & 후기

# url field만들기 O
# 없으면 출력 안시키기 O

def index(request):
    menus = Menu.objects.all()
    names = Menu.objects.values_list('name', flat=True) #모델에 있는 메뉴
    ingredients = Menu.objects.values_list('ingredient', flat=True) #모델에 있는 메뉴 재료

    new_dicts = {}
    for i in range(0, len(names)):
        new_dicts[names[i]] = ingredients[i]
    names_as_keys = list(new_dicts.keys())
    ingredients_as_values = list(new_dicts.values()) #new_dicts = {'마늘볶음밥' : '마늘, 밥, 버터', '국수' : '면, 육수'}

    ingredient_list = []
    for food in ingredients_as_values: # ingredients_as_values = '마늘, 밥, 버터', '국, 밥' , food = '마늘, 밥, 버터'
        vv = food.split(',')
        ingredient_list.append(vv)         # ingredient_list = ['마늘', '밥', '버터'], [' 국', ' 밥']

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


def search_menu_text(request):
    menus = Menu.objects.all()
    input = request.GET.get('practice_ingredient')
    one_ingredient_menuname, two_ingredient_menuname, three_ingredient_menuname, four_ingredient_menuname  = [], [], [], [] #재료가 1개인 메뉴
    one_ingredient_ingredient, two_ingredient_ingredient, three_ingredient_ingredient, four_ingredient_ingredient = [], [], [], [] #재료가 1개인 메뉴 재료 리스트

    i = 0
    q = 0

    split_my_input = input.split(', ') #밥, 마늘 -> ['밥', '마늘']
    try_menu_len = []
    try_menu = []
    for try_input in split_my_input:
        if try_input == ((list(dict_dict.values())[i])[q]):
            try_menu_len.append(try_input)
            if len(split_my_input) == len(try_menu_len):
                try_menu.append(((list(dict_dict.values())[i])))
            else:
                pass
        else:
            if q < len(list(dict_dict.values())[i]) - 1: # Situation of when input does not match with a value in a key and go to next value.
                q = q + 1
                continue

            else: #Situation of when input does not match with a value in a key until the end and go to next key and start again.
                i = i + 1
                q = 0
                continue
        i = i + 1
        q = 0



    while (i < len(list(dict_dict.keys()))):
        # split_my_input = input.split(', ') #밥, 마늘 -> ['밥', '마늘']
        # try_menu_len = []
        # try_menu = []
        # for try_input in split_my_input:
        #     if try_input == ((list(dict_dict.values())[i])[q]):
        #         try_menu_len.append(try_input)
        #         if len(split_my_input) == len(try_menu_len):
        #             try_menu.append(((list(dict_dict.values())[i])))
        #         else:
        #             pass
        #     else:
        #         if q < len(list(dict_dict.values())[i]) - 1: # Situation of when input does not match with a value in a key and go to next value.
        #             q = q + 1
        #             continue
        #
        #         else: #Situation of when input does not match with a value in a key until the end and go to next key and start again.
        #             i = i + 1
        #             q = 0
        #             continue
        #     i = i + 1
        #     q = 0

        if input == ((list(dict_dict.values())[i])[q]): #compare value in a key and see if it's same as 재료_input
            if len(list(dict_dict.values())[i]) == 1:   #찾은 key값의 value가 input일 때
                # one_ingredient_menu.append('<div class="tt">' + list(dict_dict.keys())[i] + '<span class="tt-text">' + ', '.join(list(dict_dict.keys())[i]) + '</span>' + '</div>')
                one_ingredient_menuname.append(list(dict_dict.keys())[i])
                one_ingredient_ingredient.append(list(dict_dict.values())[i])

            elif len(list(dict_dict.values())[i]) == 2: #찾은 key값의 value가 input + 재료1개 더
                two_ingredient_menuname.append(list(dict_dict.keys())[i])
                two_ingredient_ingredient.append(list(dict_dict.values())[i])

            elif len(list(dict_dict.values())[i]) == 3: #찾은 key값의 value가 input + 재료2개 더
                three_ingredient_menuname.append(list(dict_dict.keys())[i])
                three_ingredient_ingredient.append(list(dict_dict.values())[i])

            elif len(list(dict_dict.values())[i]) > 3:                                                  #찾은 key값의 value가 input + 재료3개이상
                four_ingredient_menuname.append(list(dict_dict.keys())[i])
                four_ingredient_ingredient.append(list(dict_dict.values())[i])

        else:
            if q < len(list(dict_dict.values())[i]) - 1: # Situation of when input does not match with a value in a key and go to next value.
                q = q + 1
                continue

            else: #Situation of when input does not match with a value in a key until the end and go to next key and start again.
                i = i + 1
                q = 0
                continue
        i = i + 1
        q = 0

    newnew1, newnew2, newnew3, newnew4 = {}, {}, {}, {}
    try:
        for qq in range(0, len(one_ingredient_menuname)):
            newnew1[one_ingredient_menuname[qq]] = ', '.join(one_ingredient_ingredient[qq])
    except:
        pass

    try:
        for qq in range(0, len(two_ingredient_menuname)):
            newnew2[two_ingredient_menuname[qq]] = ', '.join(two_ingredient_ingredient[qq])
    except:
        pass

    try:
        for qq in range(0, len(three_ingredient_menuname)):
            newnew3[three_ingredient_menuname[qq]] = ', '.join(three_ingredient_ingredient[qq])
    except:
        pass

    try:
        for qq in range(0, len(four_ingredient_menuname)):
            newnew4[four_ingredient_menuname[qq]] = ', '.join(four_ingredient_ingredient[qq])
    except:
        pass

    len1, len2, len3, len4 = len(one_ingredient_menuname), len(two_ingredient_menuname), len(three_ingredient_menuname), len(four_ingredient_menuname)

    context = {'input' : input, 'newnew1' : newnew1, 'newnew2' : newnew2, 'newnew3' : newnew3, 'newnew4' : newnew4,
    'input' : input, 'menus' : menus,
    'len1' : len1, 'len2' : len2, 'len3' : len3, 'len4' : len4,
    'try_menu' : try_menu
    }
    return render(request, 'foodapp/practice.html', context)


def add_menu_button(request):
    menus = Menu.objects.all()
    context = {'menus':menus}
    if request.method == 'POST':
        form = MenuForm(request.POST)
        if form.is_valid():
            obj = Menu(name=form.data['name'], ingredient=form.data['ingredient'], link=form.data['link'])
            obj.save()
            return render(request, 'foodapp/index.html', context)
        return HttpResponse('fail')

    elif request.method == 'GET':
        form = MenuForm()
        return render(request, 'foodapp/form.html', {'form': form})
    else:
        pass
