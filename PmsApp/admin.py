# coding:utf8
from django.contrib import admin
from models import *
from django.contrib.auth.admin import UserAdmin

# Register your models here.

# -*- coding: utf-8 -*-

from django.contrib import admin
from django.utils.text import capfirst
from django.utils.datastructures import SortedDict


def find_model_index(name):
    count = 0
    for model, model_admin in admin.site._registry.items():
        if capfirst(model._meta.verbose_name_plural) == name:
            return count
        else:
            count += 1
    return count


def index_decorator(func):
    def inner(*args, **kwargs):
        templateresponse = func(*args, **kwargs)
        for app in templateresponse.context_data['app_list']:
            app['models'].sort(key=lambda x: find_model_index(x['name']))
        return templateresponse
    return inner

registry = SortedDict()
registry.update(admin.site._registry)
admin.site._registry = registry
admin.site.index = index_decorator(admin.site.index)
admin.site.app_index = index_decorator(admin.site.app_index)
#admin.site.register(yourmodel, yourmodeladmin)
#*********


class UserProfileInline(admin.StackedInline):
    fk_name = 'user'
    model = UserProfile
#    can_delete = False
#    verbose_name_plural = 'profile'


# Define a new User admin
class UserAdmin(UserAdmin):
    inlines = (UserProfileInline, )


class PropertyAdmin(admin.ModelAdmin):
    list_display = ('p_name', 'p_type', 'p_ownername', 'p_ownerphone', 'p_owneremail', 'p_ownerid', 'p_manager', 'p_rent_circle', 'p_status')
    search_fields = ('p_name', 'p_owner')
    list_filter = ('p_name', 'p_status')
    ordering = ('-p_add_date',)

admin.site.register(Property, PropertyAdmin)


class PropertyPriceAdmin(admin.ModelAdmin):
    list_display = ('pp_price_name', 'pp_property', 'pp_rent_circle', 'pp_price', 'pp_currency')
    search_fields = ('pp_price_name', 'pp_property')
    list_filter = ('pp_property', 'pp_rent_circle')
    ordering = ('-pp_add_date',)

admin.site.register(PropertyPrice, PropertyPriceAdmin)


class TenantInfoAdmin(admin.ModelAdmin):
    list_display = ('t_name', 't_tpye', 't_phone', 't_email', 't_manager', 't_status')
    search_fields = ('t_name', 't_phone', 't_email', 't_manager')
    list_filter = ('t_tpye', 't_manager', 't_status')
    ordering = ('-t_date',)

admin.site.register(TenantInfo, TenantInfoAdmin)


class RentalBillAdmin(admin.ModelAdmin):
    list_display = ('rb_property', 'rb_period_start', 'rb_period_end', 'rb_should_pay_date', 'rb_actual_pay_date', 'rb_type', 'rb_tenant', 'rb_paid')
    search_fields = ('rb_property', 'rb_should_pay_date', 'rb_tenant')
    list_filter = ('rb_property', 'rb_tenant', 'rb_paid')
    ordering = ('-rb_paid', '-rb_should_pay_date')

admin.site.register(RentalBill, RentalBillAdmin)


class MaintenanceBillAdmin(admin.ModelAdmin):
    list_display = ('mb_property', 'mb_billdate', 'mb_should_pay_date', 'mb_billtype', 'mb_paid')
    search_fields = ('mb_property', 'mb_billdate', 'mb_billtype')
    list_filter = ('mb_property', 'mb_billtype', 'mb_paid')
    ordering = ('-mb_paid', '-mb_should_pay_date')

admin.site.register(MaintenanceBill, MaintenanceBillAdmin)


class ManagerCompanyAdmin(admin.ModelAdmin):
    pass

admin.site.register(ManagerCompany, ManagerCompanyAdmin)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)