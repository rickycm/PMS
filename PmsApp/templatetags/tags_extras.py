__author__ = 'ricky'
from django import template
from PmsApp.models import *

register = template.Library()


@register.filter
def getPropertyId(prop, attr):
    if isinstance(prop, Property):
        #print(prop.__dict__)
        if attr == "id":
            return prop.id
        if attr == "name":
            return prop.p_name
    else:
        print(prop)
        return ''