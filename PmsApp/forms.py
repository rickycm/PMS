#coding=utf-8
__author__ = 'ricky'

from django import forms

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
    message = forms.CharField()