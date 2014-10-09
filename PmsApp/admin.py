# coding:utf8
from django.contrib import admin
from models import *
from django.contrib.auth.admin import UserAdmin

# Register your models here.


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


class ManagerCompanyAdmin(admin.ModelAdmin):
    pass

admin.site.register(ManagerCompany, ManagerCompanyAdmin)


class TenantInfoAdmin(admin.ModelAdmin):
    pass

admin.site.register(TenantInfo, TenantInfoAdmin)


class RentalBillAdmin(admin.ModelAdmin):
    pass

admin.site.register(RentalBill, RentalBillAdmin)


class MaintanceBillAdmin(admin.ModelAdmin):
    pass

admin.site.register(MaintanceBill, MaintanceBillAdmin)


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)