from django import forms
from django.db import models
from .models import Menu
class MenuForm(forms.ModelForm):

    class Meta:
        model = Menu
        fields = ['name', 'Essential_Ingredient', 'Nonessential_Ingredient', 'link', 'tip']



    # name = forms.CharField(label='name', max_length=30)
    # Essential_Ingredient = forms.CharField(label='Essential_Ingredient',max_length = 100)
    # Nonessential_Ingredient = forms.CharField(label='Nonessential_Ingredient',max_length = 100)
    # link = forms.CharField(label = 'link',max_length = 200)
    # tip = forms.CharField(label = 'tip')
