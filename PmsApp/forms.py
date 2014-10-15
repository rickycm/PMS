#coding=utf-8
__author__ = 'ricky'

from django import forms
from django.contrib.auth.models import User
from globals import *
from models import *
from datetimewidget.widgets import DateTimeWidget
from django.contrib.admin import widgets

attrs_dict = {'class': 'required'}


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
    message = forms.CharField()


class CheckinForm(forms.Form):

    properties = forms.ModelChoiceField(queryset=Property.objects.filter(p_manager='0'), widget=forms.Select(attrs=attrs_dict))
    action = forms.ChoiceField(choices=ACTION, initial={1: u'Check-in'})
    checkinTime = forms.DateTimeField()
    prx_checkoutTime = forms.DateTimeField()

    def __init__(self, *args, **kwargs):
        userid = kwargs.pop('user')
        super(CheckinForm, self).__init__(*args, **kwargs)
        u = User.objects.filter(pk=userid)
        self.fields['properties'].choices = [('', '----------')] + [(properties.id, properties.p_name)
                            for properties in Property.objects.filter(p_manager=u)]

        #self.fields['mydate'].widget = widgets.AdminDateWidget()
        self.fields['prx_checkoutTime'].widget = widgets.AdminTimeWidget()
        self.fields['checkinTime'].widget = widgets.AdminSplitDateTime()
'''
    class Meta:
        dateTimeOptions = {
            'format': 'dd/mm/yyyy HH:ii P',
            'autoclose': True,
            'showMeridian': True
        }
        widgets = {
            #NOT Use localization and set a default format
            'checkinTime': DateTimeWidget(options=dateTimeOptions),
            'prx_checkoutTime': DateTimeWidget(options=dateTimeOptions),
        }
'''
