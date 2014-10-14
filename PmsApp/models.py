# coding:utf8
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from globals import *



class ManagerCompany(models.Model):
    mc_name = models.CharField(max_length=200, blank=True, null=True)
    mc_phone = models.CharField(max_length=20, blank=True, null=True)
    mc_address = models.CharField(max_length=200, blank=True, null=True)
    mc_email = models.EmailField(max_length=1000, verbose_name=u'E-mail', blank=True, null=True)
    mc_date = models.DateTimeField(blank=True, null=True, auto_now_add=True, verbose_name=u'Add Date')


class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True, verbose_name=u'UserProfile')
    name = models.CharField(max_length=200, blank=True, null=True)
    user_type = models.IntegerField(choices=USER_TYPE, default=1)
    type = models.IntegerField(choices=PERSON_TYPE, default=1)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=1000, verbose_name=u'E-mail', blank=True, null=True)

    m_company = models.ForeignKey(ManagerCompany, blank=True, null=True)

    def __unicode__(self):
        return self.user.username


def create_user_profile(sender, instance, created, **kwargs):
    """Create the UserProfile when a new User is saved"""
    if created:
        profile = UserProfile()
        profile.user = instance
        profile.save()

#post_save.connect(create_user_profile, sender=User)


class TenantInfo(models.Model):
    t_name = models.CharField(max_length=200, blank=True, null=True, verbose_name=u'Tenant Name')
    t_tpye = models.IntegerField(choices=PERSON_TYPE, default=1)
    t_phone = models.CharField(max_length=20, blank=True, null=True)
    t_address = models.CharField(max_length=20, blank=True, null=True)
    t_email = models.EmailField(max_length=1000, verbose_name=u'E-mail', blank=True, null=True)
    t_date = models.DateTimeField(blank=True, null=True, verbose_name=u'Add Date')

'''
class OwnerInfo(models.Model):
    o_name = models.CharField(max_length=200, blank=True, null=True)
    o_tpye = models.IntegerField(choices=PERSON_TYPE, default=1)
    o_phone = models.CharField(max_length=20, blank=True, null=True)
    o_address = models.CharField(max_length=20, blank=True, null=True)
    o_email = models.EmailField(max_length=1000, verbose_name='e-mail', blank=True, null=True)
'''


'''
class ManagerInfo(models.Model):
    m_name = models.CharField(max_length=200, blank=True, null=True)
    m_tpye = models.IntegerField(choices=PERSON_TYPE, default=1)
    m_phone = models.CharField(max_length=20, blank=True, null=True)
    m_address = models.CharField(max_length=20, blank=True, null=True)
    m_email = models.EmailField(max_length=1000, verbose_name='e-mail', blank=True, null=True)
    m_company = models.ForeignKey(ManagerCompany)
'''


class Property(models.Model):
    p_name = models.CharField(max_length=200, blank=True, null=True, verbose_name=u'Property Name')
    p_type = models.IntegerField(choices=P_TYPE, default=1, blank=True, null=True)
    p_address = models.CharField(max_length=20, blank=True, null=True)
    p_owner = models.ForeignKey(User, related_name='owner')
    p_manager = models.ForeignKey(User, related_name='manager', blank=True, null=True)
    p_tenant = models.ForeignKey(TenantInfo, blank=True, null=True)
    p_area = models.CharField(max_length=200, blank=True, null=True)
    p_buildtime = models.DateField(blank=True, null=True)
    p_rent_circle = models.IntegerField(choices=RENTAL_TYPE, default=1, blank=True, null=True)
    p_rent_price = models.IntegerField(blank=True, null=True)
    p_add_date = models.DateField(blank=True, null=True, auto_now_add=True, verbose_name=u'Add Date')
    p_status = models.IntegerField(choices=P_STATUS, default=1, blank=True, null=True)
    p_checkinTime = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = u'Property'
        verbose_name_plural = u'Properties'
        ordering = ['p_add_date']

    def __unicode__(self):
        return self.p_name


class RentalBill(models.Model):
    rb_property = models.ForeignKey(Property, verbose_name=u'Property')
    rb_period_start = models.DateField(blank=True, null=True, verbose_name=u'Start Date')
    rb_period_end = models.DateField(blank=True, null=True, verbose_name=u'End Date')
    rb_should_pay_date = models.DateField(blank=True, null=True, verbose_name=u'Due Date')
    rb_actual_pay_date = models.DateField(blank=True, null=True, verbose_name=u'Pay Date')
    rb_type = models.IntegerField(choices=RENTAL_TYPE, default=1, blank=True, null=True, verbose_name=u'Type')
    rb_payer_name = models.CharField(max_length=200, blank=True, null=True, verbose_name=u'Payer name')
    rb_note = models.CharField(max_length=2000, blank=True, null=True, verbose_name=u'Note')
    rb_actionHistory = models.ForeignKey(ActionHistory, blank=True, null=True)
    rb_date = models.DateTimeField(blank=True, null=True, auto_now_add=True, verbose_name=u'Add Date')


class MaintenanceBill(models.Model):
    mb_property = models.ForeignKey(Property)
    mb_billdate = models.DateField(blank=True, null=True)
    mb_should_pay_date = models.DateField(blank=True, null=True)
    mb_actual_pay_date = models.DateField(blank=True, null=True)
    mb_billtype = models.CharField(max_length=200, blank=True, null=True)
    mb_payer_name = models.CharField(max_length=200, blank=True, null=True)
    mb_note = models.CharField(max_length=2000, blank=True, null=True)
    mb_actionHistory = models.ForeignKey(ActionHistory, blank=True, null=True)
    mb_date = models.DateTimeField(blank=True, null=True, auto_now_add=True, verbose_name=u'Add Date')


class Deposit(models.Model):
    d_property = models.ForeignKey(Property, verbose_name=u'Property')
    d_date = models.DateTimeField(blank=True, null=True, verbose_name=u'Date')
    d_tenant = models.ForeignKey(TenantInfo, blank=True, null=True)
    d_payer_name = models.CharField(max_length=200, blank=True, null=True, verbose_name=u'Payer name')
    d_actionHistory = models.ForeignKey(ActionHistory, blank=True, null=True)
    d_date = models.DateTimeField(blank=True, null=True, auto_now_add=True, verbose_name=u'Add Date')


class ActionHistory(models.Model):
    h_property = models.ForeignKey(Property, verbose_name=u'Property')
    h_date = models.DateTimeField(blank=True, null=True, auto_now_add=True, verbose_name=u'Date')
    h_action = models.IntegerField(choices=ACTION, default=1, blank=True, null=True, verbose_name=u'Action')
    h_operator = models.ForeignKey(User, unique=True, verbose_name=u'Operator')
    h_tenant = models.ForeignKey(TenantInfo, blank=True, null=True)
    h_payer_name = models.CharField(max_length=200, blank=True, null=True, verbose_name=u'Payer name')