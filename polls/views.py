# Create your views here.
from django.http import JsonResponse, HttpRequest
from django.shortcuts import render

from polls.sevices import get_flotes, get_flote_by_name

import logging
logger = logging.getLogger(__name__)
#Flote.objects.create(name="camionee", code="2131", brand="renault", patent="212adc", status=1)

def get_flote_by_name_view(request, name):
    flote = get_flote_by_name(name)
    return JsonResponse(flote)
    #return HttpResponse(f"<h1>Hello and welcome to my first <u>{name}</u> project!</h1>")

def get_flotes_view(request):
    flotes = get_flotes()
    return JsonResponse(flotes, safe=False)

def get_home_page(request):
    return render(request, 'ti_ingreso.html')

def get_flotes_page(request):
    return render(request, 'ti_vista-flota.html')