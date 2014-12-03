#coding=utf-8
__author__ = 'ricky'
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from django import forms
from django.contrib.auth.models import User
from globals import *
from models import *
from bootstrap3_datetime.widgets import DateTimePicker
from phonenumber_field.modelfields import PhoneNumberField

from django.utils.translation import ugettext_lazy as _
from django import forms
from datetime import datetime, time, date, timedelta

from models import Property


class MultiFileInput(forms.FileInput):
    def render(self, name, value, attrs={}):
        attrs['multiple'] = 'multiple'
        return super(MultiFileInput, self).render(name, None, attrs=attrs)
    def value_from_datadict(self, data, files, name):
        if hasattr(files, 'getlist'):
            return files.getlist(name)
        else:
            return [files.get(name)]


class MultiFileField(forms.FileField):
    widget = MultiFileInput
    default_error_messages = {
        'min_num': u"Ensure at least %(min_num)s files are uploaded (received %(num_files)s).",
        'max_num': u"Ensure at most %(max_num)s files are uploaded (received %(num_files)s).",
        'file_size' : u"File: %(uploaded_file_name)s, exceeded maximum upload size."
    }
    def __init__(self, *args, **kwargs):
        self.min_num = kwargs.pop('min_num', 0)
        self.max_num = kwargs.pop('max_num', None)
        self.maximum_file_size = kwargs.pop('maximum_file_size', None)
        super(MultiFileField, self).__init__(*args, **kwargs)
    def to_python(self, data):
        ret = []
        for item in data:
            ret.append(super(MultiFileField, self).to_python(item))
        return ret
    def validate(self, data):
        super(MultiFileField, self).validate(data)
        num_files = len(data)
        if len(data) and not data[0]:
            num_files = 0
        if num_files < self.min_num:
            raise forms.ValidationError(self.error_messages['min_num'] % {'min_num': self.min_num, 'num_files': num_files})
            return
        elif self.max_num and  num_files > self.max_num:
            raise forms.ValidationError(self.error_messages['max_num'] % {'max_num': self.max_num, 'num_files': num_files})
        for uploaded_file in data:
            if uploaded_file is not None and uploaded_file.size > self.maximum_file_size:
                raise forms.ValidationError(self.error_messages['file_size'] % { 'uploaded_file_name': uploaded_file.name})


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
    message = forms.CharField()


class CheckinForm(forms.Form):

    properties = forms.ModelChoiceField(queryset=Property.objects.all(), widget=forms.Select(attrs={'class': 'required', 'onChange': 'javascript:getPrice(this.value);'}))
    #action = forms.ChoiceField(choices=ACTION, widget=forms.Select(attrs={'disabled': 'disabled'}))
    action = forms.ChoiceField(choices={(1, u'Check-in')})
    rent_circle = forms.ChoiceField(choices=RENTAL_TYPE, initial={1: u'Monthly'})
    #checkinTime = forms.DateTimeField(required=True, widget=DateTimePicker(options={"data-date-format": "YYYY-MM-DD HH:mm",
    #                                   "pickSeconds": False, "autoclose": 1, "todayBtn":  1}))
    checkinTime = forms.DateField(required=True, widget=forms.TextInput())
    circle_count = forms.IntegerField(initial=1, widget=forms.NumberInput(attrs={'class': 'required', 'onBlur': 'javascript:getCheckoutDate();'}))
    #prx_checkoutTime = forms.DateTimeField(required=True, widget=DateTimePicker(options={"data-date-format": "YYYY-MM-DD HH:mm",
    #                                        "pickSeconds": False, "autoclose": 1, "todayBtn":  1, "disabled": True}))
    prx_checkoutTime = forms.DateField(required=True, widget=forms.TextInput(attrs={'class': 'required', 'onClick': 'javascript:getCheckoutDate();', 'readonly': 'true'}))
    tenant = forms.ModelChoiceField(queryset=TenantInfo.objects.all(), widget=forms.Select(attrs={'class': 'required', 'onChange': 'javascript:setPayername();'}))
    price = forms.ModelChoiceField(queryset=PropertyPrice.objects.all(), required=True)
    deposit_amount = forms.IntegerField(required=True, initial=0)
    deposit_currency = forms.ChoiceField(choices=CURRENCY, required=True, initial='SGD')

    #payer_name = forms.CharField(required=True)

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
        #print(prx_checkoutTime)
        return cleaned_data
'''
        if prx_checkoutTime < checkinTime:
            msg = "Check-out time must be later than Check-in time."
            self.add_error('prx_checkoutTime', msg)
        else:
            return cleaned_data
'''


class CheckoutForm(forms.Form):

    action = forms.ChoiceField(choices={(2, u'Check-out')})
    checkoutTime = forms.DateField(required=True, widget=forms.TextInput())
    propertyid = forms.CharField(widget=forms.HiddenInput())

    def clean(self):
        cleaned_data = super(CheckoutForm, self).clean()
        #return cleaned_data

        if cleaned_data.get("propertyid") is not None:
            prop = Property.objects.get(pk=int(cleaned_data.get("propertyid")))
            checkoutTime = cleaned_data.get("checkoutTime")
            #checkoutTime = datetime.strptime(checkoutTimeStr, '%Y-%m-%d %H:%M:%S')
            checkinHis = ActionHistory.objects.get(pk=prop.p_last_checkinHis)
            checkinTime = checkinHis.h_checkinTime

            if checkoutTime < checkinTime:
                msg = "Check-out time must be later than Check-in time."
                self.add_error('checkoutTime', msg)
            else:
                return cleaned_data




class PropertyForm(forms.ModelForm):

    photos = MultiFileField(max_num = 10, min_num = 0, maximum_file_size = 1024*1024*5, help_text='(Select one or more Photos, png/jpg/jpeg Only, Suggest Size: 700*500.)')
    note = forms.CharField(widget=forms.Textarea(attrs={'cols':'80','rows':'3'}), label='Description', required=False)

    class Meta:
        model = Property
        fields = ('p_name', 'p_address', 'p_type', 'p_roomtype', 'p_unittype', 'p_ownername', 'p_ownerphone', 'p_owneremail', 'p_ownerid',
                  'p_buildtime', 'p_rent_circle', 'p_status', 'photos', 'note')

    def clean_photos(self):
        photos = self.cleaned_data['photos']
        for photo in photos:
            if photo is not None and not photo.name.lower().endswith('.png') and not photo.name.lower().endswith('.jpg') and not photo.name.lower().endswith('.jpeg'):
                raise forms.ValidationError('png/jpg/jpeg only')
        return photos

    def clean(self):
        cleaned_data = super(PropertyForm, self).clean()
        return cleaned_data


class TenantForm(forms.ModelForm):

    t_phone = forms.CharField(widget=forms.NumberInput, label='Phone')

    class Meta:
        model = TenantInfo
        fields = ('t_name', 't_gender', 't_nationality', 't_ethnic', 't_profession', 't_phone', 't_address', 't_email')

    def clean(self):
        cleaned_data = super(TenantForm, self).clean()
        #phone = cleaned_data.get('t_phone')

        return cleaned_data


class PropertyPriceForm(forms.ModelForm):

    pp_currency = forms.ChoiceField(choices=CURRENCY, required=True, initial='SGD', label='Currency')

    class Meta:
        model = PropertyPrice
        fields = ('pp_property', 'pp_price_name', 'pp_rent_circle', 'pp_price', 'pp_currency')

    def clean(self):
        cleaned_data = super(PropertyPriceForm, self).clean()

        return cleaned_data