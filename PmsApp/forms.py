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

    properties = forms.ModelChoiceField(queryset=Property.objects.all(), widget=forms.Select(attrs={'class': 'required', 'onChange': 'javascript:getPrice(this.value);'}))
    action = forms.ChoiceField(choices=ACTION, initial={1: u'Check-in'})
    checkinTime = forms.DateTimeField(required=True, widget=DateTimePicker(options={"data-date-format": "YYYY-MM-DD HH:mm",
                                       "pickSeconds": False, "autoclose": 1, "todayBtn":  1}))
    prx_checkoutTime = forms.DateTimeField(required=True, widget=DateTimePicker(options={"data-date-format": "YYYY-MM-DD HH:mm",
                                       "pickSeconds": False, "autoclose": 1, "todayBtn":  1}))
    tenant = forms.ModelChoiceField(queryset=TenantInfo.objects.all(), widget=forms.Select(attrs=attrs_dict))
    rent_circle = forms.ChoiceField(choices=RENTAL_TYPE, initial={1: u'Monthly'})
    price = forms.ModelChoiceField(queryset=PropertyPrice.objects.all(), widget=forms.Select(attrs={'class': 'required'}))

    def __init__(self, *args, **kwargs):
        userid = kwargs.pop('user')
        try:
            propid = kwargs.pop('propid')
        except:
            propid = ''
        u = User.objects.filter(pk=userid)
        super(CheckinForm, self).__init__(*args, **kwargs)
        if propid:
            self.fields['properties'].choices = [(properties.id, properties.p_name)
                                for properties in Property.objects.filter(pk=propid)]
            self.fields['price'].choices = [(price.id, str(price.pp_currency)+': '+str(price.pp_price)+' - '+str(price.pp_price_name)+'('+str(price.get_pp_rent_circle_display())+')')
                                            for price in PropertyPrice.objects.filter(pp_property=propid)]
        else:
            self.fields['properties'].choices = [('', '----------')] + [(properties.id, properties.p_name)
                                for properties in Property.objects.filter(p_manager=u)]
        self.fields['tenant'].choices = [('', '----------')] + [(tenantinfo.id, tenantinfo.t_name)
                                for tenantinfo in TenantInfo.objects.filter(t_manager=u)]

    def clean(self):
        cleaned_data = super(CheckinForm, self).clean()
        checkinTime = cleaned_data.get("checkinTime")
        prx_checkoutTime = cleaned_data.get("prx_checkoutTime")

        if prx_checkoutTime < checkinTime:
            msg = "Check-out time must be later than Check-in time."
            self.add_error('prx_checkoutTime', msg)
        else:
            return cleaned_data


class CheckoutForm(forms.Form):

    propertyid = forms.HiddenInput()
    checkoutTime = forms.DateTimeField(required=True, widget=DateTimePicker(options={"data-date-format": "YYYY-MM-DD HH:mm",
                                       "pickSeconds": False, "autoclose": 1, "todayBtn":  1}))

    def clean(self):
        cleaned_data = super(CheckinForm, self).clean()
        return cleaned_data
        '''
        checkoutTime = cleaned_data.get("prx_checkoutTime")

        if prx_checkoutTime < checkinTime:
            msg = "Check-out time must be later than Check-in time."
            self.add_error('prx_checkoutTime', msg)
        else:
            return cleaned_data
        '''
