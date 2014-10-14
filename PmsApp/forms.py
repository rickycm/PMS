#coding=utf-8
__author__ = 'ricky'

from django import forms
from globals import *
from models import *

attrs_dict = {'class': 'required'}


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
    message = forms.CharField()


class CheckinForm(forms.Form):
需修改
    def __init__(self, *args, **kwargs):
        super(CheckinForm, self).__init__(*args, **kwargs)
        self.fields['property'].choices = [('', '----------')] + [(property.p_name, property.p_status) for property in Property.objects.all()]

    property = forms.ChoiceField(choices=(), widget=forms.Select(attrs=attrs_dict))
    action = forms.IntegerField(choices=ACTION, default=1)