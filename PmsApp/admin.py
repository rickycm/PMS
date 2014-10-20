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
    pass

admin.site.register(Property, PropertyAdmin)


class PropertyPriceAdmin(admin.ModelAdmin):
    pass

admin.site.register(PropertyPrice, PropertyPriceAdmin)


class TenantInfoAdmin(admin.ModelAdmin):
    pass

admin.site.register(TenantInfo, TenantInfoAdmin)


class RentalBillAdmin(admin.ModelAdmin):
    pass

admin.site.register(RentalBill, RentalBillAdmin)


class MaintenanceBillAdmin(admin.ModelAdmin):
    pass

admin.site.register(MaintenanceBill, MaintenanceBillAdmin)


class ManagerCompanyAdmin(admin.ModelAdmin):
    pass

admin.site.register(ManagerCompany, ManagerCompanyAdmin)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)