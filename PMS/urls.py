#coding=utf-8
from django.conf.urls import patterns, include, url
from PmsApp import views
from PMS import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'PMS.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_PATH}),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index),
    url(r'^property/list/$', views.property_list),
    (r'^accounts/logout/$', views.logout_view),
    (r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    (r'^login-form/$', views.login_form),
    #(r'^accounts/', include('userena.urls')),
)
