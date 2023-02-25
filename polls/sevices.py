import json
from django.core import serializers
from django.contrib.auth import authenticate, login
from django.contrib import messages
from datetime import datetime
from datetime import date
from .forms import *
from .models import *

import logging
logger = logging.getLogger(__name__)

FLOTES_IMAGES = {
    'RETROESCAVADORA': "images/retro.jpg",
    'CAMIONETA': "images/cam.jpg",
    'CARRETÓN': "images/carre.jpg",
    'TANQUE REGADOR': "images/tar.jpg",
    'TANQUE DE COMBUSTIBLE': "images/tac.jpg",
    'MOTONIVELADORA': "images/motn.jpg",
    'CAMIÓN': "images/can.jpg",
}

FLOTE_CODES = ["RET01", "RET02", "RET03", "CON01", "CAM01", "CAM02", "CAM03",
            "CAM04", "CAM05", "CAM06", "CAM07", "MOT01"]


def get_type_name(type):
    for t in FLOTE_TYPES:
        if type == t[0]:
            return t[1]


def flotes():
    flotes = Flote.objects.values_list('pk', 'type', 'status')
    res = {}
    for type in FLOTE_TYPES:
        res[type[1]] = {'flotes': []}
        res[type[1]]['image_file'] = FLOTES_IMAGES[type[1]]
    for flote in flotes:
        flote_type = get_type_name(flote[1])
        attrs = {'code': flote[0],
                'yel': flote[2]=='YEL', 'red': flote[2]=='RED', 'gre': flote[2]=='GRE'}
        res[flote_type]['flotes'].append(attrs)
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
    res = []
    query = list(Maintenance.objects.filter(flote__code=code))
    query.sort(key=lambda x: x.date, reverse=True)
    query = to_json(query)
    for maintenance in query:
        pk = maintenance["pk"]
        maintenance = maintenance["fields"]
        maintenance["pk"] = pk
        if maintenance["type"] == "REP":
            maintenance["type"] = "Reparación"
        else:
            maintenance["type"] = "Mantenimiento"
        if maintenance["oil"]:
            maintenance["oil"] = "Se cambio el aceite"
        else:
            maintenance["oil"] = ""
        if maintenance["filter"]:
            maintenance["filter"] = "Se cambio el filtro"
        else:
            maintenance["filter"] = ""
        res.append(maintenance)

    return res


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
    main_nots = get_maintenance_notifications(flote)
    alert_nots = get_alert_notifications(flote)
    return main_nots + alert_nots


def get_alert_notifications(flote):
    res = []
    flote_alerts = Alert.objects.filter(flote=flote)
    for alert in flote_alerts:
        delta = get_delta_days(alert.limit_date)
        notify = generate_alert_notify(alert, delta)
        if notify:
            res.append(notify)

    return res


def generate_alert_notify(alert, delta):
    msg = ""
    if delta == 0:
        msg = "La fecha limite se cumple hoy."
    elif delta > 0:
        msg = f"Alerta vencida por {delta} dias."
    elif delta >= -7 :
        msg = f"Quedan {abs(delta)} dias para la fecha limite"
    if msg:
        return {"title": alert.title,
                "msg": f"{alert.description}. " + msg}


def get_maintenance_notifications(flote):
    notifications = []
    if flote.code in FLOTE_CODES:
        last_main_oil = get_last_maintenance_of(flote, 'oil')
        last_main_filter = get_last_maintenance_of(flote, 'filter')
        if need_maintenance(last_main_oil):
            notify = generate_maintenance_notify(
                last_main_oil, flote.code, 'aceite')
            if notify:
                notifications.append(notify)
        if need_maintenance(last_main_filter):
            notify = generate_maintenance_notify(
                last_main_filter, flote.code, 'filtro')
            if notify:
                notifications.append(notify)

    return notifications


def get_last_maintenance_of(flote, field):
    maintenances = Maintenance.objects.filter(flote=flote, **{field: True})
    if maintenances:
        return maintenances.latest('date')


def need_maintenance(maintenance):
    if maintenance:
        delta_days = get_delta_days(maintenance.date)
        if delta_days >= 23:
            return True
    else:
        return True


def get_delta_days(date1):
    return (date.today() - date1).days


def generate_maintenance_notify(last_main, code, of_what):
    if last_main:
        delta_days = (date.today() - last_main.date).days
        msg = f"La flota {code} tuvo su ultimo mantenimiento de {of_what} hace {delta_days} dias."
    else:
        msg = f"La flota no tiene mantenimientos de {of_what}"
    return {"title": "Mantenimiento", "msg": msg}


def get_alerts():
    alerts = list(Alert.objects.all())
    alerts.sort(key=lambda x: x.limit_date)
    alerts = to_json(alerts)
    return format_alerts(alerts)


def get_alerts_by_flote(code):
    alerts = list(Alert.objects.filter(flote__code=code))
    alerts.sort(key=lambda x: x.limit_date)
    alerts = to_json(alerts)
    return format_alerts(alerts)

def get_alert_by_pk(pk):
    alert = Alert.objects.get(pk=pk)
    if alert:
        return alert


def format_alerts(alerts):
    res = []
    for alert in alerts:
        pk = alert["pk"]
        alert = alert["fields"]
        alert["pk"] = pk
        res.append(alert)
    return res
