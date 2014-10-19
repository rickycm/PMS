#coding=utf-8
import logging, json, time
from datetime import datetime

from django.utils import timezone
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect

from PmsApp import forms

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
            return render_to_response("index.html", {'user': user})
            #return HttpResponseRedirect("/")
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
    return render_to_response("index.html", {'user': user}, context_instance=RequestContext(request))


def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")


@login_required
def property_list(rq):
    properties = []

    user = rq.user
    if user.is_superuser == 1:
        properties = Property.objects.all()
        print('user' + user.username + 'len(properties) = ' + str(len(properties)))

        return render_to_response("property_table.html",
                                  {'title': 'Property List', 'user': user, 'properties': properties}, context_instance=RequestContext(rq))
    else:
        properties = Property.objects.filter(p_manager=user)
        print('user' + user.username + 'len(properties) = ' + str(len(properties)))

        return render_to_response("property_table.html",
                                  {'title': 'Property List', 'user': user, 'properties': properties}, context_instance=RequestContext(rq))


@login_required
def checkinForm(rq):
    user = rq.user

    if rq.method == 'GET':
        propid = rq.GET.get('propertyid')
        if propid != None:
            try:
                this_property = Property.objects.get(pk=propid)
            except Property.DoesNotExist:
                title = u'Error'
                errorMessage = u'Property Does not Exist!'
                return render_to_response("errorMessage.html", {'errorMessage': errorMessage, 'title': title},
                                      context_instance=RequestContext(rq))
            form = forms.CheckinForm(instance=this_property, user=user.id)
        else:
            form = forms.CheckinForm(user=user.id)

        return render_to_response('checkinForm.html', {'title': u'Check-in', 'form': form},
                              context_instance=RequestContext(rq))
    else:
        form = forms.CheckinForm(rq.POST, user=user.id)
        print(form.data['checkinTime'])
        checkintime = time.strptime(form.data['checkinTime'], "%Y-%m-%d %H:%M")
        #checkouttime = datetime.strptime(form.data['prx_checkoutTime'], "%Y-%m-%d %H:%M")
        print(time.strftime("%Y-%m-%d-%H-%M", checkintime))
        if form.is_valid():
            prop = Property.objects.get(pk=form.data['properties'])
            print(prop)
            tenant = TenantInfo.objects.get(pk=form.data['tenant'])
            actionhis = ActionHistory.objects.create(
                h_property = prop,
                h_action = form.data['action'],
                h_operator = user,
                h_tenant = tenant,
                h_checkinTime = form.data['checkinTime'],
                h_prox_checkoutTime = form.data['prx_checkoutTime'],
            )
            actionhis.save()
            print(actionhis)
            prop.p_checkinTime = form.data['checkinTime']
            prop.p_status = 2
            prop.p_tenant = tenant
            prop.p_rent_circle = form.data['rent_circle']
            prop.save()
            print(prop)
            return HttpResponseRedirect('/action/?actionid='+str(actionhis.id))
        else:
            logger.debug('Setting form is invalid.')
            return render_to_response('checkinForm.html', {'title': u'Check-in', 'form': form}, context_instance=RequestContext(rq))



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