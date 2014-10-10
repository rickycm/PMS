from django.shortcuts import render, render_to_response
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    productName = ' '
    return render_to_response('index.html', {'productName': productName})


def property_list(request):
    return render_to_response('property_table.html', {'productName': ''})
    #return render_to_response('tables.html', {'productName': ''})
