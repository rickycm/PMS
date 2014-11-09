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
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),

    url(r'^admin/', include(admin.site.urls)),
    #url(r'', include('multiuploader.urls')),
    url(r'^$', views.index),
    url(r'^property/list/$', views.property_list),
    url(r'^checkinForm/$', views.checkin),
    (r'^checkoutForm/$', views.checkout),
    (r'^accounts/logout/$', views.logout_view),
    (r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    (r'^login-form/$', views.login_form),
    (r'^propertyPrice_list/$', views.propertyPrice_list),
    (r'^propertyDetail/$', views.propertyDetail),
    (r'^getCheckoutDate/$', views.getCheckoutDate),
    (r'^billList/$', views.propertyRentalBillList),
    (r'^payBill/$', views.payBill),
    (r'^payBill_reverse/$', views.payBill_reverse),
    (r'^allBill_list/$', views.allBill_list),
    (r'^tenantList/$', views.tenantList),
    (r'^deleteTenant/$', views.deleteTenant),
    (r'^propertyForm/$', views.propertyForm),
    (r'^propertyFormEdit/$', views.propertyFormEdit),
    (r'^tenantForm/$', views.tenantForm),
    (r'^tenantFormEdit/$', views.tenantFormEdit),
    (r'^deleteProperty/$', views.deleteProperty),

    #(r'^accounts/', include('userena.urls')),
    #(r'^property/$', views.PropertyList.as_view()),
    #(r'^patients/(?P<pk>[0-9]+)/$', views.PatientDetail.as_view()),
    #url(r'^datetime/$', views.datetime),  # test
)
