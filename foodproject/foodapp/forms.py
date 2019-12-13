from django import forms
from django.db import models

class MenuForm(forms.Form):
    name = forms.CharField(label='name', max_length=30)
    ingredient = forms.CharField(label='ingredient')
    link = forms.URLField(max_length=200, label = 'link')
