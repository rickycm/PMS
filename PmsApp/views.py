#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import logging, json
import hashlib
from datetime import time, date, timedelta

from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.utils import dateparse,timezone
from django.db.models import Q

from StringIO import StringIO

from PmsApp import forms, addMonth

from PmsApp.models import *

logger = logging.getLogger('django.dev')


def login_form(request):
    try:
        username = request.POST['login_username']
        password = request.POST['login_password']
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            form = forms.LoginForm(request.POST)
            login(request, user)
            # Redirect to a success page.
            #return render_to_response("index.html", {'user': user})
            return HttpResponseRedirect("/")
        else:
            form = forms.LoginForm()
            # Return an error message.
            return render_to_response("login.html", {'msg': "请重新输入账户", 'form':form}, context_instance = RequestContext(request))
    except:
        form = forms.LoginForm()
        return render_to_response("login.html", {'msg': "请重新登录", 'form':form}, context_instance = RequestContext(request))


@login_required
def index(request):
    user = request.user
    propertyCount = Property.objects.filter(Q(p_manager=user), ~Q(p_status=-1)).count()
    propertylist = Property.objects.filter(Q(p_manager=user), Q(p_status=1))
    print(propertylist)
    tenantCount = TenantInfo.objects.filter(t_manager=user).count()
    billToPayCount = 0
    #bill_list = RentalBill.objects.toPayListOfManger(pay=0, userId=user.id, startdate=addMonth.datetime_offset_by_month(date.today(), -1), enddate=date.today())
    #bill_list = RentalBill.objects.toPayListOfManger(pay=0, userId=user.id)
    bill_list = RentalBill.objects.filter(Q(rb_manager=user), Q(rb_paid=0))

    billToPayCount = bill_list.count()
    #print(propertyCount, tenantCount, billToPayCount)

    import datetime
    now = datetime.datetime.now()
    billlist = []
    for bill in bill_list:
        if now.month == bill.rb_should_pay_date.month:
            billlist.append(bill)

    return render_to_response("index.html", {'user': user, 'propertyCount': propertyCount, 'tenantCount': tenantCount, 'billofmonth': billlist,
                                             'billToPayCount': billToPayCount, 'properties': propertylist}, context_instance=RequestContext(request))



def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")


@login_required
def property_list(rq):
    properties = []

    user = rq.user
    if user.is_superuser == 1:
        properties = Property.objects.all()
        #print('user' + user.username + 'len(properties) = ' + str(len(properties)))

        return render_to_response("property_table.html",
                                  {'title': 'Property List', 'user': user, 'properties': properties}, context_instance=RequestContext(rq))
    else:
        properties = Property.objects.filter(Q(p_manager=user), ~Q(p_status=-1))
        #print('user' + user.username + 'len(properties) = ' + str(len(properties)))

        return render_to_response("property_table.html",
                                  {'title': 'Property List', 'user': user, 'properties': properties}, context_instance=RequestContext(rq))


@login_required
def propertyRentalBillList(rq):
    user = rq.user

    propertyid = int(rq.GET.get('propertyid'))
    this_property = Property.objects.get(pk=propertyid)

    rentalbillList_paid = RentalBill.objects.filter(rb_property=propertyid, rb_paid=1)
    rentalbillList_notpaid = RentalBill.objects.filter(rb_property=propertyid, rb_paid=0)

    return render_to_response("allBill_list.html",
                                  {'title': 'Rental Bill List', 'user': user, 'notPaidBillList': rentalbillList_notpaid, 'paidBillList': rentalbillList_paid}, context_instance=RequestContext(rq))


@login_required
def allBill_list(rq):
    user = rq.user
    properties = Property.objects.filter(p_manager=user)
    notPaidBillList = []
    paidBillList = []
    for this_property in properties:
        rentalbillList_paid = RentalBill.objects.filter(rb_property=this_property, rb_paid=1)
        rentalbillList_notpaid = RentalBill.objects.filter(rb_property=this_property, rb_paid=0)
        for rnp in rentalbillList_notpaid:
            notPaidBillList.append(rnp)
        for rp in rentalbillList_paid:
            paidBillList.append(rp)

    return render_to_response("allBill_list.html",
                                  {'title': 'Rental Bill List', 'user': user, 'notPaidBillList': notPaidBillList, 'paidBillList': paidBillList}, context_instance=RequestContext(rq))


@login_required
def payBill(rq):
    user = rq.user
    method = rq.GET.get('method')
    backurl = rq.GET.get('backurl')
    #paid = int(rq.GET.get('paid'))
    propertyid = int(rq.GET.get('propertyid'))
    this_property = Property.objects.get(pk=propertyid)
    billid = int(rq.GET.get('billid'))

    if method == 'pay':
        this_bill = RentalBill.objects.get(pk=billid)
        #this_bill.rb_actual_pay_date = datetime.today()
        this_bill.rb_paid = 1
        this_bill.save()

        this_property.p_billsNotPaid = this_property.p_billsNotPaid-1
        this_property.save()
    elif method == 'r_pay':
        this_bill = RentalBill.objects.get(pk=billid)
        #this_bill.rb_actual_pay_date = datetime.today()
        this_bill.rb_paid = 0
        this_bill.save()

        this_property.p_billsNotPaid = this_property.p_billsNotPaid+1
        this_property.save()
    elif method == 'delete':

        this_bill = RentalBill.objects.get(pk=billid)
        #this_bill.rb_actual_pay_date = datetime.today()
        if this_bill.rb_paid == 0:
            this_property.p_billsNotPaid = this_property.p_billsNotPaid-1
            this_property.save()

        this_bill.rb_paid = -1
        this_bill.save()


    rentalbillList_paid = RentalBill.objects.filter(rb_property=propertyid, rb_paid=1)
    rentalbillList_notpaid = RentalBill.objects.filter(rb_property=propertyid, rb_paid=0)

    return HttpResponseRedirect(backurl)
    return render_to_response(backurl,
                                  {'title': 'Rental Bill List', 'user': user, 'rentalbillList_paid': rentalbillList_paid,
                                   'rentalbillList_notpaid': rentalbillList_notpaid, 'property': this_property}, context_instance=RequestContext(rq))


@login_required
def payBill_reverse(rq):
    user = rq.user
    backurl = rq.GET.get('backurl')
    #paid = int(rq.GET.get('paid'))
    propertyid = int(rq.GET.get('propertyid'))
    this_property = Property.objects.get(pk=propertyid)
    billid = int(rq.GET.get('billid'))

    this_bill = RentalBill.objects.get(pk=billid)
    #this_bill.rb_actual_pay_date = datetime.today()
    this_bill.rb_paid = 0
    this_bill.save()

    this_property.p_billsNotPaid = this_property.p_billsNotPaid+1
    this_property.save()

    rentalbillList_paid = RentalBill.objects.filter(rb_property=propertyid, rb_paid=1)
    rentalbillList_notpaid = RentalBill.objects.filter(rb_property=propertyid, rb_paid=0)
    return HttpResponseRedirect(backurl)
    return render_to_response(backurl,
                                  {'title': 'Rental Bill List', 'user': user, 'rentalbillList_paid': rentalbillList_paid,
                                   'rentalbillList_notpaid': rentalbillList_notpaid, 'property': this_property}, context_instance=RequestContext(rq))


@login_required
def checkin(rq):
    user = rq.user
    backurl = rq.get_full_path()
    if rq.method == 'GET':
        propid = rq.GET.get('propertyid')
        if propid != None:
            try:
                this_property = Property.objects.get(pk=propid)
            except Property.DoesNotExist:
                title = u'Error'
                errorMessage = u'Property Does not Exist!'
                return render_to_response("errorMessage.html", {'errorMessage': errorMessage, 'title': title, 'backurl': backurl},
                                      context_instance=RequestContext(rq))
            form = forms.CheckinForm(propid=propid, user=user.id, initial={'action': '1'})
        else:
            form = forms.CheckinForm(user=user.id, initial={'action': '1'})

        return render_to_response('checkinForm.html', {'title': u'Check-in', 'form': form},
                              context_instance=RequestContext(rq))
    else:
        form = forms.CheckinForm(rq.POST, user=user.id, initial={'action': '1'})
        if form.is_valid():
            #checkintime = time.strptime(form.data['checkinTime'], "%Y-%m-%d %H:%M")
            #checkouttime = datetime.strptime(form.data['prx_checkoutTime'], "%Y-%m-%d %H:%M")
            prop = Property.objects.get(pk=form.data['properties'])
            tenant = TenantInfo.objects.get(pk=form.data['tenant'])
            priceid = form.data['price']
            actionhis = ActionHistory.objects.create(
                h_property = prop,
                h_action = form.data['action'],
                h_operator = user,
                h_tenant = tenant.id,
                h_checkinTime = form.data['checkinTime'],
                h_prox_checkoutTime = form.data['prx_checkoutTime'],
                h_checkinPrice = priceid,
                h_pay_circle = form.data['rent_circle'],
                h_circle_count = form.data['circle_count'],
            )
            actionhis.save()

            deposit = Deposit.objects.create(
                d_property = prop,
                d_amount = form.data['deposit_amount'],
                d_currency = form.data['deposit_currency'],
                d_tenant = tenant,
                #d_payer_name = form.data['payer_name'],
                d_payer_name = tenant.t_name,
                d_actionHistory = actionhis,

            )
            deposit.save()

            #Generate Bill
            for i in range(int(form.data['circle_count'])):
                checkinTime = dateparse.parse_date(form.data['checkinTime'])
                if form.data['rent_circle'] == '1':
                    billdate = addMonth.datetime_offset_by_month(checkinTime, i)
                    period_end = addMonth.datetime_offset_by_month(checkinTime, i+1)
                elif form.data['rent_circle'] == '2':
                    billdate = addMonth.datetime_offset_by_month(checkinTime, i*3)
                    period_end = addMonth.datetime_offset_by_month(checkinTime, (i+1)*3)
                elif form.data['rent_circle'] == '3':
                    billdate = addMonth.datetime_offset_by_month(checkinTime, i*12)
                    period_end = addMonth.datetime_offset_by_month(checkinTime, (i+1)*12)
                elif form.data['rent_circle'] == '4':
                    billdate = checkinTime + timedelta(days=i)
                    period_end = billdate + timedelta(days=i+1)

                rb = RentalBill.objects.create(
                    rb_property = prop,
                    rb_property_name = prop.p_name,
                    rb_period_start = billdate,
                    rb_period_end = period_end,
                    rb_should_pay_date = billdate,
                    rb_type = form.data['rent_circle'],
                    rb_tenant = tenant,
                    rb_actionHistory = actionhis,
                    rb_manager_id = user.id,
                )
                rb.save()

            prop.p_checkinTime = form.data['checkinTime']
            prop.p_last_checkinHis = actionhis.id
            prop.p_status = 2
            prop.p_tenant = tenant
            prop.p_billsNotPaid = int(form.data['circle_count'])
            prop.save()

            msg = u'Check-In Success!'
            #return HttpResponseRedirect('/action/?actionid='+str(actionhis.id))
            return render_to_response('checkinForm.html', {'title': u'Check-in', 'form': form, 'msg': msg},
                              context_instance=RequestContext(rq))
        else:
            logger.debug('Setting form is invalid.')
            return render_to_response('checkinForm.html', {'title': u'Check-in', 'form': form}, context_instance=RequestContext(rq))


def datetime(rq):
    return render_to_response("datetime.html")


def propertyPrice_list(request):
    price_list = []
    property_id = request.GET['property_id']
    prices = PropertyPrice.objects.filter(pp_property = property_id)
    for price in prices:
        c = {}
        c['text'] = str(price.pp_currency)+': '+str(price.pp_price)+' - '+str(price.pp_price_name)+'('+str(price.get_pp_rent_circle_display())+')'
        c['value'] = price.id
        price_list.append(c)
    return HttpResponse(json.dumps(price_list))


def getCheckoutDate(request):
    checkoutdate = ''
    checkinDate = dateparse.parse_date(request.GET['checkinDate'])
    #checkinDate = datetime.strptime(request.GET['checkinDate'])
    rentCircle = request.GET['rentCircle']
    circleCount = int(request.GET['circleCount'])

    if rentCircle == '1':
        checkoutdate = addMonth.datetime_offset_by_month(checkinDate, circleCount)
    elif rentCircle == '2':
        checkoutdate = addMonth.datetime_offset_by_month(checkinDate, circleCount*3)
    elif rentCircle == '3':
        checkoutdate = addMonth.datetime_offset_by_month(checkinDate, circleCount*12)
    elif rentCircle == '4':
        checkoutdate = checkinDate + timedelta(days=circleCount)

    #checkoutdate = checkoutdate.replace(hour=checkinDate.hour, minute=checkinDate.minute)
    #return HttpResponse(checkoutdate.strftime("%Y-%m-%d %H:%M"))
    return HttpResponse(checkoutdate.strftime("%Y-%m-%d"))


@login_required
def checkout(rq):
    user = rq.user
    backurl = rq.get_full_path()

    if rq.method == 'GET':
        propid = rq.GET.get('propertyid')
        if propid != None:
            try:
                this_property = Property.objects.get(pk=propid)
                checkinhis = this_property.p_last_checkinHis
            except Property.DoesNotExist:
                title = u'Error'
                errorMessage = u'Property Does not Exist!'
                return render_to_response("errorMessage.html", {'errorMessage': errorMessage, 'title': title, 'backurl': backurl},
                                      context_instance=RequestContext(rq))
            form = forms.CheckoutForm(initial={'propertyid': propid, 'action': '2'})
            return render_to_response('checkoutForm.html', {'title': u'Check-out', 'form': form, 'property': this_property, 'checkinhis': checkinhis, 'propertyid': propid},
                              context_instance=RequestContext(rq))
        else:
            title = u'Error'
            errorMessage = u'Property Does not Exist!'
            backurl = rq.path
            return render_to_response("errorMessage.html", {'errorMessage': errorMessage, 'title': title, 'backurl': backurl},
                                      context_instance=RequestContext(rq))
    else:
        form = forms.CheckoutForm(rq.POST)
        propid = rq.GET.get('propertyid')
        if propid != None:
            try:
                prop = Property.objects.get(pk=propid)
                checkinhis = ActionHistory.objects.get(pk=prop.p_last_checkinHis)
            except Property.DoesNotExist:
                title = u'Error'
                errorMessage = u'Property Does not Exist!'
                return render_to_response("errorMessage.html", {'errorMessage': errorMessage, 'title': title, 'backurl': backurl},
                                      context_instance=RequestContext(rq))

            if form.is_valid():
                actionhis = ActionHistory.objects.create(
                    h_property = prop,
                    h_action = 2,
                    h_operator = user,
                    h_tenant = checkinhis.h_tenant,
                    h_checkinTime = checkinhis.h_checkinTime,
                    h_checkinPrice = checkinhis.h_checkinPrice,
                    h_prox_checkoutTime = checkinhis.h_prox_checkoutTime,
                    h_checkoutTime = form.data['checkoutTime'],
                )
                actionhis.save()
                prop.p_checkinTime = ''
                prop.p_status = 1
                prop.p_tenant = None
                prop.save()
                msg = u'Check-out Success!'
                #return HttpResponseRedirect('/action/?actionid='+str(actionhis.id))
                return render_to_response('checkoutForm.html', {'title': u'Check-out', 'form': form, 'msg': msg, 'propertyid': prop.id},
                                  context_instance=RequestContext(rq))
            else:
                logger.debug(u'Check-out Failed.')
                return render_to_response('checkoutForm.html', {'title': u'Check-out', 'form': form, 'property': prop, 'checkinhis': checkinhis, 'propertyid': prop.id},
                                  context_instance=RequestContext(rq))
        else:
            title = u'Error'
            errorMessage = u'Property Does not Exist!'
            backurl = rq.path
            return render_to_response("errorMessage.html", {'errorMessage': errorMessage, 'title': title, 'backurl': backurl},
                                      context_instance=RequestContext(rq))


@login_required
def propertyDetail(rq):
    user = rq.user
    backurl = rq.get_full_path()

    if rq.method == 'GET':
        propid = rq.GET.get('propertyid')
        if propid != None:
            try:
                this_property = Property.objects.get(pk=propid)
                photo_list = PropertyPhoto.objects.filter(propertyid=propid)
                if this_property.p_status == 1:
                    if this_property.p_last_checkoutHis:
                        checkInOuthis = ActionHistory.objects.get(pk=this_property.p_last_checkoutHis)
                        price = PropertyPrice.objects.get(pk=checkInOuthis.h_checkinPrice)
                        priceStr = str(price.pp_currency)+': '+str(price.pp_price)+' - '+str(price.pp_price_name)+'('+str(price.get_pp_rent_circle_display())+')'
                        tenant = checkInOuthis.h_tenant
                    else:
                        checkInOuthis = None
                        priceStr = ''
                        tenant = None
                elif this_property.p_status == 2:
                    if this_property.p_last_checkinHis:
                        checkInOuthis = ActionHistory.objects.get(pk=this_property.p_last_checkinHis)
                        price = PropertyPrice.objects.get(pk=checkInOuthis.h_checkinPrice)
                        priceStr = str(price.pp_currency)+': '+str(price.pp_price)+' - '+str(price.pp_price_name)+'('+str(price.get_pp_rent_circle_display())+')'
                        tenant = checkInOuthis.h_tenant
                    else:
                        checkInOuthis = None
                        priceStr = ''
                        tenant = None
                else:
                    checkInOuthis = None
                    priceStr = ''
                    tenant = None

            except Property.DoesNotExist:
                title = u'Error'
                errorMessage = u'Oops! Property Does not Exist!'
                return render_to_response("errorMessage.html", {'errorMessage': errorMessage, 'title': title, 'backurl': backurl},
                                      context_instance=RequestContext(rq))


            return render_to_response('propertyDetail.html', {'title': u'Property Detail', 'property': this_property, 'checkInOuthis': checkInOuthis,
                                                              'priceStr': priceStr, 'tenant': tenant, 'photoList': photo_list}, context_instance=RequestContext(rq))
        else:
            title = u'Error'
            errorMessage = u'Property Does not Exist!'
            backurl = rq.get_full_path()
            return render_to_response("errorMessage.html", {'errorMessage': errorMessage, 'title': title, 'backurl': backurl},
                                      context_instance=RequestContext(rq))


def handle_uploaded_image(i):
    import os
    from django.core.files import File
    from PIL import Image, ImageFile
    # resize image
    imagefile  = StringIO(i.read())
    imageImage = Image.open(imagefile)

    (width, height) = imageImage.size
    (width, height) = scale_dimensions(width, height, longest_side=500)

    resizedImage = imageImage.resize((width, height))

    imagefile = StringIO()
    resizedImage.save(imagefile,'JPEG')
    filename = hashlib.md5(imagefile.getvalue()).hexdigest()+'.jpg'

    # #save to disk
    imagefile = open(os.path.join('/Users/ricky/PycharmProjects/PMS/PMS/media',filename), 'w')
    resizedImage.save(imagefile,'JPEG', quality=90)
    imagefile = open(os.path.join('/Users/ricky/PycharmProjects/PMS/PMS/media',filename), 'r')
    content = File(imagefile)
    print(filename)
    return (filename, content)


def scale_dimensions(width, height, longest_side):
    if width > height:
        if width > longest_side:
            ratio = longest_side*1./width
            return (int(width*ratio), int(height*ratio))
    elif height > longest_side:
        ratio = longest_side*1./height
        return (int(width*ratio), int(height*ratio))
    return (width, height)


@login_required
@csrf_protect
def propertyForm(rq):
    user = rq.user
    backurl = rq.get_full_path()

    if rq.method == 'GET':
        propidStr = rq.GET.get('propertyid')
        if propidStr:
            propid = int(propidStr)
            try:
                this_property = Property.objects.get(pk=propid)
                form = forms.PropertyForm(instance=this_property)
            except:
                form = forms.PropertyForm()
        else:
            form = forms.PropertyForm()

        return render_to_response('propertyForm.html', {'title': u'Property Form', 'form': form}, context_instance=RequestContext(rq))
    else:
        form = forms.PropertyForm(rq.POST, rq.FILES);
        if form.is_valid():

            new_property = Property.objects.create(
                p_name = form.data['p_name'],
                p_type = int(form.data['p_type']),
                p_address = form.data['p_address'],
                p_ownername = form.data['p_ownername'],
                p_ownerphone = form.data['p_ownerphone'],
                p_owneremail = form.data['p_owneremail'],
                p_ownerid = form.data['p_ownerid'],
                p_manager = user,
                p_buildtime = form.data['p_buildtime'],
                p_rent_circle = int(form.data['p_rent_circle']),
                p_status = int(form.data['p_status']),
                p_billsNotPaid = 0,
                p_note = form.data['note'],
            )
            new_property.save()

            file_list = rq.FILES.getlist('photos')
            for afile in file_list:

                photofile = PropertyPhoto()
                #handle_uploaded_image(afile)
                photofile.photofile = afile
                photofile.propertyid = new_property.id
                photofile.save()
                print(afile.name)
                print(photofile.photofile.url)

            msg = u'Add Property Success!'
            #return HttpResponseRedirect('/action/?actionid='+str(actionhis.id))
            return render_to_response('propertyDetail.html', {'title': u'Property Detail', 'property': new_property}, context_instance=RequestContext(rq))
        else:
            logger.debug(u'Add Property Failed.')
            return render_to_response('propertyForm.html', {'title': u'Property Form', 'form': form}, context_instance=RequestContext(rq))


@login_required
@csrf_protect
def propertyFormEdit(rq):
    user = rq.user
    backurl = rq.get_full_path()
    propidStr = rq.GET.get('propertyid')

    prop = get_object_or_404(Property, pk=int(propidStr))

    if rq.method == 'POST':
        form = forms.PropertyForm(rq.POST, instance = prop)
        if form.is_valid():
            prop = form.save()

            file_list = rq.FILES.getlist('photos')
            for afile in file_list:

                photofile = PropertyPhoto()
                #handle_uploaded_image(afile)
                photofile.photofile = afile
                photofile.propertyid = prop.id
                photofile.save()

            return HttpResponseRedirect('/property/list')

    return render_to_response('propertyForm.html', {'title': u'Property Form', 'propertyid': propidStr, 'form': forms.PropertyForm(instance = prop)}, context_instance=RequestContext(rq))


@login_required
def deleteProperty(rq):
    user = rq.user
    propid = int(rq.GET.get('propertyid'))
    this_property = Property.objects.get(pk=propid)
    this_property.p_status = -1
    this_property.p_billsNotPaid = 0
    this_property.save()

    billList = RentalBill.objects.filter(rb_property=this_property)
    for bl in billList:
        bl.rb_paid = -1
        bl.save()

    return HttpResponseRedirect('/property/list/')


@login_required
@csrf_protect
def tenantForm(rq):
    user = rq.user
    backurl = rq.get_full_path()

    if rq.method == 'GET':
        tenantIdStr = rq.GET.get('tenantId')
        if tenantIdStr:
            tenantId = int(tenantIdStr)
            try:
                tenant = TenantInfo.objects.get(pk=tenantId)
                form = forms.TenantForm(instance=tenant)
            except:
                form = forms.TenantForm()
        else:
            form = forms.TenantForm()

        return render_to_response('tenantForm.html', {'title': u'Tenant Form', 'form': form}, context_instance=RequestContext(rq))
    else:
        form = forms.TenantForm(rq.POST)
        if form.is_valid():
            new_tenant = TenantInfo.objects.create(
                t_name = form.data['t_name'],
                #t_tpye = int(form.data['t_tpye']),
                t_phone = form.data['t_phone'],
                t_address = form.data['t_address'],
                t_email = form.data['t_email'],
                t_manager = user,
                t_gender = form.data['t_gender'],
                t_nationality = form.data['t_nationality'],
                t_ethnic = form.data['t_ethnic'],
                t_profession = form.data['t_profession'],
            )
            new_tenant.save()
            msg = u'Add Tenant Success!'
            return HttpResponseRedirect('/tenantList')
            #return render_to_response('propertyDetail.html', {'title': u'Property Detail', 'property': new_property}, context_instance=RequestContext(rq))
        else:
            logger.debug(u'Add Tenant Failed.')
            return render_to_response('tenantForm.html', {'title': u'Tenant Form', 'form': form}, context_instance=RequestContext(rq))


@login_required
@csrf_protect
def tenantFormEdit(rq):
    user = rq.user
    backurl = rq.get_full_path()
    tenantIdStr = rq.GET.get('tenantId')

    tenant = get_object_or_404(TenantInfo, pk=int(tenantIdStr))

    if rq.method == 'POST':
        form = forms.TenantForm(rq.POST, instance = tenant)
        if form.is_valid():
            tenant = form.save()

            return HttpResponseRedirect('/tenantList')

    return render_to_response('tenantFormEdit.html', {'title': u'Tenant Form', 'tenantId': tenantIdStr, 'form': forms.TenantForm(instance = tenant)}, context_instance=RequestContext(rq))


@login_required
def tenantList(rq):
    user = rq.user

    if user.is_superuser == 1:
        tenantlist = TenantInfo.objects.all()
    else:
        tenantlist = TenantInfo.objects.filter(Q(t_manager=user), ~Q(t_status=-1))

    return render_to_response("tenantList.html",
                                  {'title': 'Tenant List', 'user': user, 'tenantlist': tenantlist}, context_instance=RequestContext(rq))


@login_required
def deleteTenant(rq):
    user = rq.user
    tenantid = int(rq.GET.get('tenantId'))
    this_tenant = TenantInfo.objects.get(pk=tenantid)
    this_tenant.t_status = -1
    this_tenant.save()

    return HttpResponseRedirect('/tenantList')


@login_required
@csrf_protect
def priceForm(rq):
    user = rq.user
    backurl = rq.get_full_path()

    if rq.method == 'GET':
        priceIdStr = rq.GET.get('priceId')
        if priceIdStr:
            priceId = int(priceIdStr)
            try:
                propertyPrice = PropertyPrice.objects.get(pk=priceId)
                form = forms.PropertyPriceForm(user=user.id, instance=propertyPrice)
            except:
                form = forms.PropertyPriceForm(user=user.id)
        else:
            form = forms.PropertyPriceForm(user=user.id)

        return render_to_response('priceForm.html', {'title': u'Property Price Form', 'form': form}, context_instance=RequestContext(rq))
    else:
        form = forms.PropertyPriceForm(rq.POST, user=user.id)
        if form.is_valid():
            property = get_object_or_404(Property, pk=int(form.data['pp_property']))
            new_price = PropertyPrice.objects.create(
                pp_property = property,
                pp_price_name = form.data['pp_price_name'],
                pp_rent_circle = form.data['pp_rent_circle'],
                pp_price = form.data['pp_price'],
                pp_currency = form.data['pp_currency'],
                pp_manager = user,
            )
            new_price.save()
            msg = u'Add Price Success!'
            return HttpResponseRedirect('/priceList')
            #return render_to_response('propertyDetail.html', {'title': u'Property Detail', 'property': new_property}, context_instance=RequestContext(rq))
        else:
            logger.debug(u'Add Price Failed.')
            return render_to_response('priceForm.html', {'title': u'Property Price Form', 'form': form}, context_instance=RequestContext(rq))


@login_required
@csrf_protect
def priceFormEdit(rq):
    user = rq.user
    backurl = rq.get_full_path()
    priceIdStr = rq.GET.get('priceId')

    price = get_object_or_404(PropertyPrice, pk=int(priceIdStr))

    if rq.method == 'POST':
        form = forms.PropertyPriceForm(rq.POST, instance = price, user=user.id)
        if form.is_valid():
            price = form.save()

            return HttpResponseRedirect('/priceList')

    return render_to_response('priceForm.html', {'title': u'Property Price Form', 'priceId': priceIdStr, 'form': forms.PropertyPriceForm(instance = price, user=user.id)}, context_instance=RequestContext(rq))


@login_required
def priceList(rq):
    user = rq.user
    if user.is_superuser == 1:
        priceList = PropertyPrice.objects.all()

    else:
        priceList = PropertyPrice.objects.filter(pp_manager=user)

    return render_to_response("priceList.html",
                                  {'title': 'Price List', 'user': user, 'priceList': priceList}, context_instance=RequestContext(rq))


@login_required
def deletePrice(rq):
    user = rq.user
    priceid = int(rq.GET.get('priceId'))
    price = PropertyPrice.objects.get(pk=priceid)
    price.delete()

    return HttpResponseRedirect('/priceList')


'''
from rest_framework.views import APIView
from rest_framework.response import Response
#from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from serializers import PropertySerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


class PropertyList(APIView):

    # 在setting文件中间配置的话，就没有必要在这个地方强制指定了。
    #renderer_classes = [JSONRenderer, BrowsableAPIRenderer]

    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        # 这里每个医生访问的应该只是他自己的病人
        # 尚未考虑如何解决分页问题。
        #patients = patient.objects.filter(doctor_id=request.user.id, p_state__lt=10)
        properties = Property.objects.all();
        serializer = PropertySerializer(properties, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        # 不出意外的话，医生的ID信息不会包括在提交数据中，此处需要加上。
        serializer = PropertySerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PatientDetail(APIView):

    permission_classes = [IsOwner]

    def __get_object(self, pk):
        try:
            return patient.objects.get(pk=pk)
        except patient.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        person = self.__get_object(pk)
        serializer = PatientSerializer(person)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        person = self.__get_object(pk)
        serializer = PatientSerializer(person, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        person = self.__get_object(pk)
        person.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
'''