from django.db import models
from django.contrib.auth.models import User

P_TYPE = [(1, u'Apartment'), (2, u'House'), (3, u'Villa')]
P_STATUS = [(1, u'Empty'), (2, u'Rented'), (3, u'')]

class property(models.Model):
    p_name = models.CharField(max_length=200, blank=True, null=True)
    p_type = models.IntegerField(choices=P_TYPE, default=1, blank=True, null=True)
    p_owner = models.ForeignKey(User)
    p_manager = models.ForeignKey(User, blank=True, null=True)
    p_tenant = models.ForeignKey(tenantInfo, blank=True, null=True)
    p_area = models.IntegerField(blank=True, null=True)
    p_buildtime = models.DateField(blank=True, null=True)
    p_status = models.IntegerField(choices=P_STATUS, default=1, blank=True, null=True)
'''
    p_rentHistory = models.TextField(max_length=2000, blank=True, null=True)
    p_phone = models.CharField(max_length=20, blank=True, null=True)
    p_Econtact = models.CharField(max_length=20, blank=True, null=True)
    p_email = models.EmailField(max_length=1000, verbose_name='e-mail', blank=True, null=True)
    p_conception = models.DateField(blank=True, null=True)
    p_addtime = models.DateTimeField(auto_now=True, blank=True, null=True)
    doctor_id = models.CharField(max_length=20, blank=True, null=True)
'''

class tenantInfo(models.Model):
    t_name = models.CharField(max_length=200, blank=True, null=True)
    t_phone = models.CharField(max_length=20, blank=True, null=True)
    t_address = models.CharField(max_length=20, blank=True, null=True)
    t_email = models.EmailField(max_length=1000, verbose_name='e-mail', blank=True, null=True)