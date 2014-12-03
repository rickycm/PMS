# coding:utf8
from django.db import models, connection
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from globals import *


class RentalBillManager(models.Manager):
    def toPayListOfManger(self, **kwargs):
        pay = kwargs["pay"]
        userId = kwargs["userId"]
        cursor = connection.cursor()
        if "startdate" in kwargs:
            startdate = kwargs["startdate"]
            enddate = kwargs["enddate"]
            if pay == 0:
                cursor.execute("""
                    select bill.*, prop.*
                    from PmsApp_RentalBill as bill left join PmsApp_Property as prop on bill.rb_property_id=prop.id
                    where prop.p_manager_id=%s and bill.rb_paid=0 and bill.rb_should_pay_date>=%s and bill.rb_should_pay_date<%s
                    group by bill.id order by bill.rb_should_pay_date""", [userId, startdate, enddate])
            elif pay == 1:
                cursor.execute("""
                    select bill.*, prop.*
                    from PmsApp_RentalBill as bill left join PmsApp_Property as prop on bill.rb_property_id=prop.id
                    where prop.p_manager_id=%s and bill.rb_paid=1 and bill.rb_should_pay_date>=%s and bill.rb_should_pay_date<%s
                    group by bill.id order by bill.rb_should_pay_date""", [userId, startdate, enddate])
        else:
            if pay == 0:
                cursor.execute("""
                    select bill.*, prop.*
                    from PmsApp_RentalBill as bill left join PmsApp_Property as prop on bill.rb_property_id=prop.id
                    where prop.p_manager_id=%s and bill.rb_paid=0
                    group by bill.id order by bill.rb_should_pay_date""", [userId])
            elif pay == 1:
                cursor.execute("""
                    select bill.*, prop.*
                    from PmsApp_RentalBill as bill left join PmsApp_Property as prop on bill.rb_property_id=prop.id
                    where prop.p_manager_id=%s and bill.rb_paid=1
                    group by bill.id order by bill.rb_should_pay_date""", [userId])
        list = cursor.fetchall()
        return list


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
    t_name = models.CharField(max_length=200, verbose_name=u'Tenant Name')
    t_tpye = models.IntegerField(choices=PERSON_TYPE, default=1, verbose_name=u'Type')
    t_gender = models.CharField(max_length=20, choices=GENDER_CHOICE, default=u'M', verbose_name=u'Gender')
    t_nationality = models.CharField(max_length=100, blank=True, null=True , verbose_name=u'Nationality')
    t_ethnic = models.CharField(max_length=100, blank=True, null=True , verbose_name=u'Ethnic')
    t_profession = models.CharField(max_length=100, blank=True, null=True , verbose_name=u'Profession')
    t_phone = models.CharField(max_length=20, blank=True, null=True , verbose_name=u'Phone')
    t_address = models.CharField(max_length=2000, blank=True, null=True, verbose_name=u'Address')
    t_email = models.EmailField(max_length=1000, blank=True, null=True, verbose_name=u'E-mail')
    #t_leaseCommencement = models.DateField(blank=True, null=True, verbose_name=u'lease commencement')
    t_date = models.DateTimeField(blank=True, null=True, verbose_name=u'Add Date')
    t_manager = models.ForeignKey(User, related_name=u'Manager', verbose_name=u'Manager')
    t_status = models.IntegerField(choices=TENANTSTATUS, default=1, verbose_name=u'Status')

    def __unicode__(self):
        return self.t_name

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
    p_name = models.CharField(max_length=200, verbose_name=u'Property Name')
    p_type = models.IntegerField(choices=P_TYPE, default=1, verbose_name=u'Property Type')
    p_address = models.CharField(max_length=2000, blank=True, null=True, verbose_name=u'Address')
    #p_owner = models.ForeignKey(User, related_name=u'owner', verbose_name=u'Owner')
    p_ownername = models.CharField(max_length=200, verbose_name=u'Owner Name')
    p_ownerphone = models.CharField(max_length=20, blank=True, null=True, verbose_name=u'Owner Phone Number')
    p_owneremail = models.EmailField(max_length=1000, blank=True, null=True, verbose_name=u'Owner E-mail')
    p_ownerid = models.CharField(max_length=200, blank=True, null=True, verbose_name=u'Owner ID')
    p_manager = models.ForeignKey(User, related_name=u'Property manager', verbose_name=u'Manager')
    p_tenant = models.ForeignKey(TenantInfo, blank=True, null=True, verbose_name=u'Tenant')
    #p_area = models.CharField(max_length=200, blank=True, null=True, verbose_name=u'Area')
    p_roomtype = models.CharField(max_length=200, blank=True, null=True, verbose_name=u'Room Type')
    p_unittype = models.CharField(max_length=200, blank=True, null=True, verbose_name=u'Unit Type')
    p_buildtime = models.DateField(verbose_name=u'Available From')
    p_rent_circle = models.IntegerField(choices=RENTAL_TYPE, default=1, blank=True, null=True, verbose_name=u'Rent Circle')
    p_add_date = models.DateField(blank=True, null=True, auto_now_add=True, verbose_name=u'Add Date')
    p_status = models.IntegerField(choices=P_STATUS, default=1, verbose_name=u'Property Status')
    p_current_price = models.IntegerField(blank=True, null=True)
    p_last_checkinHis = models.IntegerField(blank=True, null=True)
    p_last_checkoutHis = models.IntegerField(blank=True, null=True)
    p_billsNotPaid = models.IntegerField(blank=True, null=True)
    p_note = models.TextField(blank=True, null=True, verbose_name=u'Description')

    class Meta:
        verbose_name = u'Property'
        verbose_name_plural = u'Properties'
        ordering = ['p_add_date']

    def __unicode__(self):
        return self.p_name
'''
    def __str__(self):
        return self.id
'''


class PropertyPhoto(models.Model):
    photofile = models.FileField(upload_to='photos/%Y%m')
    propertyid = models.IntegerField()
    uploadtime = models.DateTimeField(blank=True, null=True, auto_now_add=True)


class PropertyPrice(models.Model):
    pp_property = models.ForeignKey(Property, verbose_name=u'Property')
    pp_price_name = models.CharField(max_length=200, blank=True, null=True, verbose_name=u'Price Name')
    pp_rent_circle = models.IntegerField(choices=RENTAL_TYPE, default=1, blank=True, null=True, verbose_name=u'Rent Circle')
    pp_price = models.IntegerField(default=0, verbose_name=u'Price')
    pp_currency = models.CharField(max_length=10, verbose_name=u'Currency')
    pp_manager = models.ForeignKey(User, related_name=u'Property Manager', verbose_name=u'Manager')
    pp_add_date = models.DateField(blank=True, null=True, auto_now_add=True, verbose_name=u'Add Date')

    def __unicode__(self):
        return self.pp_price_name


class ActionHistory(models.Model):
    h_property = models.ForeignKey(Property, verbose_name=u'Property')
    h_date = models.DateTimeField(blank=True, null=True, auto_now_add=True, verbose_name=u'Date')
    h_action = models.IntegerField(choices=ACTION, default=1, blank=True, null=True, verbose_name=u'Action')
    h_operator = models.ForeignKey(User, verbose_name=u'Operator')
    h_tenant = models.IntegerField(blank=True, null=True)
    h_payer_name = models.CharField(max_length=200, blank=True, null=True, verbose_name=u'Payer name')
    h_checkinTime = models.DateField(blank=True, null=True, verbose_name=u'Check-in Time')
    h_checkinPrice = models.IntegerField(blank=True, null=True)
    h_prox_checkoutTime = models.DateField(blank=True, null=True, verbose_name=u'Prox Check-out Time')
    h_checkoutTime = models.DateField(blank=True, null=True, verbose_name=u'Check-out Time')
    h_pay_circle = models.IntegerField(choices=RENTAL_TYPE, default=1, blank=True, null=True, verbose_name=u'Pay Circle')
    h_circle_count = models.IntegerField(blank=True, null=True, verbose_name=u'Circle Count')


class RentHistory(models.Model):
    rh_property = models.ForeignKey(Property, verbose_name=u'Property')
    rh_tenant = models.ForeignKey(TenantInfo, blank=True, null=True, verbose_name=u'Tenant')
    rh_checkin_date = models.DateTimeField(blank=True, null=True, auto_now_add=True, verbose_name=u'Check-in Date')
    rh_checkout_date = models.DateTimeField(blank=True, null=True, auto_now_add=True, verbose_name=u'Check-out Date')
    rh_rent_circle = models.IntegerField(choices=RENTAL_TYPE, default=1, blank=True, null=True, verbose_name=u'Pay Circle')
    rh_price = models.IntegerField(blank=True, null=True, verbose_name=u'Price')
    rh_total_amount = models.IntegerField(blank=True, null=True, verbose_name=u'Total Amount')
    rh_operator = models.ForeignKey(User, unique=True, verbose_name=u'Operator')


class Deposit(models.Model):
    d_property = models.ForeignKey(Property, verbose_name=u'Property')
    d_amount = models.IntegerField(blank=True, null=True, verbose_name=u'Deposit Amount')
    d_currency = models.CharField(max_length=10, blank=True, null=True, verbose_name=u'Currency')
    d_tenant = models.ForeignKey(TenantInfo, blank=True, null=True)
    d_payer_name = models.CharField(max_length=200, blank=True, null=True, verbose_name=u'Payer name')
    d_actionHistory = models.ForeignKey(ActionHistory, blank=True, null=True)
    d_date = models.DateTimeField(blank=True, null=True, auto_now_add=True, verbose_name=u'Add Date')


class RentalBill(models.Model):
    rb_property = models.ForeignKey(Property, verbose_name=u'Property')
    rb_period_start = models.DateField(blank=True, null=True, verbose_name=u'Start Date')
    rb_period_end = models.DateField(blank=True, null=True, verbose_name=u'End Date')
    rb_should_pay_date = models.DateField(blank=True, null=True, verbose_name=u'Due Date')
    rb_actual_pay_date = models.DateField(auto_now=True, blank=True, null=True, verbose_name=u'Pay Date')
    rb_type = models.IntegerField(choices=RENTAL_TYPE, default=1, blank=True, null=True, verbose_name=u'Type')
    rb_tenant = models.ForeignKey(TenantInfo, verbose_name=u'Tenant')
    rb_payer_name = models.CharField(max_length=200, blank=True, null=True, verbose_name=u'Payer name')
    rb_note = models.CharField(max_length=2000, blank=True, null=True, verbose_name=u'Note')
    rb_paid = models.IntegerField(choices=PAID, default=0, verbose_name=u'Status')
    rb_actionHistory = models.ForeignKey(ActionHistory, blank=True, null=True)
    rb_date = models.DateTimeField(blank=True, null=True, auto_now_add=True, verbose_name=u'Add Date')

    objects = RentalBillManager()

    def __unicode__(self):
        return self.rb_property.p_name + ' / ' + self.rb_tenant.t_name + ' / ' + str(self.rb_should_pay_date)


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
    mb_paid = models.IntegerField(choices=PAID, default=0, verbose_name=u'Status')