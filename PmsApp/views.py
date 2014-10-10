#coding=utf-8
import logging
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
        print('user' + user + 'len(properties) = ' + str(len(properties)))

        return render_to_response("property_table.html",
                                  {'title': 'Property List', 'user': user, 'properties': properties}, context_instance=RequestContext(rq))
    else:
        properties = Property.objects.filter(p_manager=user)
        print('user' + user + 'len(properties) = ' + str(len(properties)))

        return render_to_response("property_table.html",
                                  {'title': 'Property List', 'user': user, 'properties': properties}, context_instance=RequestContext(rq))
