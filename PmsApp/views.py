from django.shortcuts import render, render_to_response

def index(request):
    productName = ' '
    return render_to_response('index.html', {'productName': productName})
