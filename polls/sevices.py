import json
from django.core import serializers
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import *

import logging
logger = logging.getLogger(__name__)

def flotes():
    flotes = Flote.objects.all()
    flotes = to_json(flotes)
    logger.error(flotes)
    return flotes

def flote_by_name(name):
    flotes = Flote.objects.filter(name=name)
    flotes = to_json(flotes)
    logger.error(flotes[0])
    return flotes[0]

def flote_create(request):
    name = request.POST['name']
    code = request.POST['code']
    brand = request.POST['brand']
    model = request.POST['model']
    characteristics = request.POST['characteristics']
    patent = request.POST['patent']
    production_year = request.POST['production_year']
    engine_number = request.POST['engine_number']
    chassis_number = request.POST['chassis_number']
    status = request.POST['status']
    justifyStatus = request.POST['justifyStatus']
    operators = request.POST['operators']
    views = request.POST['views']

def to_json(entities):
    if entities:
        entities = serializers.serialize('json', entities)
        entities = json.loads(entities)
    return entities

def login_service(request, username, password):
    user = authenticate(request, username=username, password=password)
    redirect_url = '/home/flotes'
    if user:
        login(request, user)
    else:
        messages.success(request, "Usuario o Contraseña erroneos, por favor intente de nuevo.")
        redirect_url = '/home/'
    return redirect_url