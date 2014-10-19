#coding=utf-8
__author__ = 'ricky'

from django import forms
from django.contrib.auth.models import User
from globals import *
from models import *
from bootstrap3_datetime.widgets import DateTimePicker

attrs_dict = {'class': 'required'}


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
    message = forms.CharField()


class CheckinForm(forms.Form):

    properties = forms.ModelChoiceField(queryset=Property.objects.all(), widget=forms.Select(attrs={'class': 'required', 'onChange': 'javascript:alert(this.value);getPrice(this.value);'}))
    action = forms.ChoiceField(choices=ACTION, initial={1: u'Check-in'})
    checkinTime = forms.DateTimeField(required=False, widget=DateTimePicker(options={"data-date-format": "YYYY-MM-DD HH:mm",
                                       "pickSeconds": False, "autoclose": 1, "todayBtn":  1}))
    prx_checkoutTime = forms.DateTimeField(required=False, widget=DateTimePicker(options={"data-date-format": "YYYY-MM-DD HH:mm",
                                       "pickSeconds": False, "autoclose": 1, "todayBtn":  1}))
    tenant = forms.ModelChoiceField(queryset=TenantInfo.objects.all(), widget=forms.Select(attrs=attrs_dict))
    rent_circle = forms.ChoiceField(choices=RENTAL_TYPE, initial={1: u'Monthly'})
    price = forms.ModelChoiceField(queryset=PropertyPrice.objects.all(), widget=forms.Select(attrs={'class': 'required'}))

    def __init__(self, *args, **kwargs):
        userid = kwargs.pop('user')
        u = User.objects.filter(pk=userid)
        super(CheckinForm, self).__init__(*args, **kwargs)
        self.fields['properties'].choices = [('', '----------')] + [(properties.id, properties.p_name)
                            for properties in Property.objects.filter(p_manager=u)]
        self.fields['tenant'].choices = [('', '----------')] + [(tenantinfo.id, tenantinfo.t_name)
                            for tenantinfo in TenantInfo.objects.filter(t_manager=u)]

    def clean(self):
        cleaned_data = super(CheckinForm, self).clean()
        print(cleaned_data)
        checkinTime = cleaned_data.get("checkinTime")
        prx_checkoutTime = cleaned_data.get("prx_checkoutTime")
        print(cleaned_data.get("properties"))
        print(cleaned_data.get("tenant"))
        print(cleaned_data.get("price"))

        if prx_checkoutTime < checkinTime:
            msg = "Check-out time must be later than Check-in time."
            print(msg)
            self.add_error('prx_checkoutTime', msg)
        else:
            return cleaned_data
