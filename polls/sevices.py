import json
from django.core import serializers
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import *

import logging
logger = logging.getLogger(__name__)

FLOTES_IMAGES = {
    'RETROESCAVADORA': "retro.png",
    'CAMIONETA': "cam.png",
    'CARRETÓN': "carre.png",
    'TANQUE REGADOR': "tar.png",
    'TANQUE DE COMBUSTIBLE': "tac.png",
    'MOTONIVELADORA': "motn.png",
    'CAMIÓN': "can.png",
}

def get_type_name(type):
    for t in FLOTE_TYPES:
        if type == t[0]:
            return t[1]

def flotes():
    import ipdb;ipdb.set_trace()
    flotes = Flote.objects.all()
    flotes = to_json(flotes)
    res = {}
    for type in FLOTE_TYPES:
        res[type[1]] = {'flotes': []}
        res[type[1]]['image_file'] = FLOTES_IMAGES[type[1]]
    for flote in flotes:
        flote_type = get_type_name(flote['fields']['type'])
        flote['fields']['code'] = flote['pk']
        res[flote_type]['flotes'].append(flote['fields'])
    logger.error(res)
    return res

def flote_by_code(code):
    flotes = Flote.objects.filter(code=code)
    json_flotes = to_json(flotes)
    res = None
    image = None
    if json_flotes:
        res = json_flotes[0]['fields']
        images = Image.objects.filter(flote=flotes[0])
        if images:
            image = images[0].image.url
            res['img'] = image
        res['code'] = json_flotes[0]['pk']
        print(res)
        return res

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