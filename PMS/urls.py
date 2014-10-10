from django.conf.urls import patterns, include, url
from PmsApp.views import *
from PMS import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'PMS.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_PATH}),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', index),
    url(r'^property/list/$', property_list),
    #(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    (r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    #(r'^accounts/', include('userena.urls')),
)
