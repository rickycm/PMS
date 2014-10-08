from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

P_TYPE = [(1, u'Apartment'), (2, u'House'), (3, u'Villa')]
P_STATUS = [(1, u'Free to rent'), (2, u'Rented'), (3, u'')]
PERSON_TYPE = [(1, u'Person'), (2, u'Company'), (3, u'Family')]
RENTAL_TYPE = [(1, u'Monthly'), (2, u'Quarterly'), (3, u'Yearly')]
USER_TYPE = [(1, u'Manager'), (2, u'Owner'), (3, u'Tenant')]


class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True, verbose_name=u'UserProfile')
    name = models.CharField(max_length=200, blank=True, null=True)
    user_type = models.IntegerField(choices=USER_TYPE, default=1)
    type = models.IntegerField(choices=PERSON_TYPE, default=1)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=1000, verbose_name='e-mail', blank=True, null=True)

    m_company = models.ForeignKey(ManagerCompany, blank=True, null=True)

    def __unicode__(self):
        return self.user.username


def create_user_profile(sender, instance, created, **kwargs):
    """Create the UserProfile when a new User is saved"""
    if created:
        profile = UserProfile()
        profile.user = instance
        profile.save()

post_save.connect(create_user_profile, sender=User)

'''
class TenantInfo(models.Model):
    t_name = models.CharField(max_length=200, blank=True, null=True)
    t_tpye = models.IntegerField(choices=PERSON_TYPE, default=1)
    t_phone = models.CharField(max_length=20, blank=True, null=True)
    t_address = models.CharField(max_length=20, blank=True, null=True)
    t_email = models.EmailField(max_length=1000, verbose_name='e-mail', blank=True, null=True)


class OwnerInfo(models.Model):
    o_name = models.CharField(max_length=200, blank=True, null=True)
    o_tpye = models.IntegerField(choices=PERSON_TYPE, default=1)
    o_phone = models.CharField(max_length=20, blank=True, null=True)
    o_address = models.CharField(max_length=20, blank=True, null=True)
    o_email = models.EmailField(max_length=1000, verbose_name='e-mail', blank=True, null=True)
'''


class ManagerCompany(models.Model):
    mc_name = models.CharField(max_length=200, blank=True, null=True)
    mc_phone = models.CharField(max_length=20, blank=True, null=True)
    mc_address = models.CharField(max_length=200, blank=True, null=True)
    mc_email = models.EmailField(max_length=1000, verbose_name='e-mail', blank=True, null=True)

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
    p_name = models.CharField(max_length=200, blank=True, null=True)
    p_type = models.IntegerField(choices=P_TYPE, default=1, blank=True, null=True)
    p_address = models.CharField(max_length=20, blank=True, null=True)
    p_owner = models.ForeignKey(User, related_name='owner')
    p_manager = models.ForeignKey(User, related_name='manager', blank=True, null=True)
    p_tenant = models.ForeignKey(User, blank=True, null=True)
    p_area = models.CharField(max_length=200, blank=True, null=True)
    p_buildtime = models.DateField(blank=True, null=True)
    p_status = models.IntegerField(choices=P_STATUS, default=1, blank=True, null=True)
    p_rent_circle = models.IntegerField(choices=RENTAL_TYPE, default=1, blank=True, null=True)
    p_rent_price = models.IntegerField(blank=True, null=True)


class RentalBill(models.Model):
    rb_property = models.ForeignKey(Property)
    rb_period_start = models.DateField(blank=True, null=True)
    rb_period_end = models.DateField(blank=True, null=True)
    rb_should_pay_date = models.DateField(blank=True, null=True)
    rb_actual_pay_date = models.DateField(blank=True, null=True)
    rb_type = models.IntegerField(choices=RENTAL_TYPE, default=1, blank=True, null=True)
    rb_payer_name = models.CharField(max_length=200, blank=True, null=True)
    rb_note = models.CharField(max_length=2000, blank=True, null=True)
