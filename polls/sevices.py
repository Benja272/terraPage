import json
from django.core import serializers
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from datetime import date, timedelta
from .forms import *
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
    return res


def flote_by_code(code):
    flotes = Flote.objects.filter(code=code)
    flote_in_db = None
    if flotes:
        flote_in_db = flotes.first()

    json_flotes = to_json(flotes)
    res = None
    if json_flotes:
        json_flotes = fix_operators(json_flotes)
        res = json_flotes[0]['fields']
        res['code'] = json_flotes[0]['pk']
        res['images'] = get_flote_images(flotes[0])
        for type in FLOTE_TYPES:
            if res['type'] == type[0]:
                res['type'] = type[1]
        return res, flote_in_db
    else:
        return None, None


def fix_operators(json_flotes):
    operators = json_flotes[0]['fields']['operators'].replace('"', '')
    operators = operators[1:len(operators)-1]
    json_flotes[0]['fields']['operators'] = operators
    return json_flotes


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
        messages.success(
            request, "Usuario o Contraseña erroneos, por favor intente de nuevo.")
        redirect_url = '/home/'
    return redirect_url


def maintenances(code):
    query = list(Maintenance.objects.filter(flote__code=code))
    query.sort(key=lambda x: x.date, reverse=True)
    for maintenance in query:
        if maintenance.type == "REP":
            maintenance.type = "Reparación"
        else:
            maintenance.type = "Mantenimiento"
        if maintenance.oil:
            maintenance.oil = "Se cambio el aceite"
        else:
            maintenance.oil = ""
        if maintenance.filter:
            maintenance.filter = "Se cambio el filtro"
        else:
            maintenance.filter = ""

    return query


def create_images(flote, files):
    for image in files:
        if not Image.objects.filter(flote=flote, image=image):
            Image.objects.create(flote=flote, image=image)


def get_flote_images(flote):
    res = None
    images = Image.objects.filter(flote=flote)
    if images:
        res = map(lambda x: {'url': x.image.url, 'pk': x.pk}, images)
    return res


def generate_notifications(flote):
    notifications = []
    last_main_oil = get_last_maintenance_of(flote, 'oil')
    last_main_filter = get_last_maintenance_of(flote, 'filter')
    if need_maintenance(last_main_oil):
        notifications.append(generate_notify(last_main_oil, flote.code, 'aceite'))
    if need_maintenance(last_main_filter):
        notifications.append(generate_notify(last_main_filter, flote.code, 'filtro'))

    return notifications


def get_last_maintenance_of(flote, field):
    maintenances = Maintenance.objects.filter(flote=flote, **{field: True})
    if maintenances:
        return maintenances.latest('date')


def need_maintenance(maintenance):
    if maintenance:
        delta_days = (date.today() - maintenance.date).days
        if delta_days >= 23:
            return True
    else:
        return True


def generate_notify(last_main, code, of_what):
    if last_main:
        delta_days = (date.today() - last_main.date).days
        return f"La flota con codigo {code} tuvo su ultimo mantenimiento de {of_what} hace {delta_days} dias."
    else:
        return f"La flota no tiene mantenimientos de {of_what}"
