from distutils.command.build_scripts import first_line_re
import json
from django.core import serializers
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse

from polls.sevices import get_flotes, get_flote_by_name
from .models import Operator, Flote

import logging
logger = logging.getLogger(__name__)
#Flote.objects.create(name="camioneta", code="2121", brand="renault", patent="212adc", status=1)

def get_flote_by_name_view(request, name):
    flote = get_flote_by_name(name)
    return JsonResponse(flote)
    #return HttpResponse(f"<h1>Hello and welcome to my first <u>{name}</u> project!</h1>")

def get_flotes_view(request):
    flotes = get_flotes()
    return JsonResponse(flotes, safe=False)

