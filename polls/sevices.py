import json
from django.core import serializers
from .models import *

import logging
logger = logging.getLogger(__name__)

def flotes():
    flotes = Flote.objects.all()
    flotes = serializers.serialize('json', flotes)
    flotes = json.loads(flotes)
    logger.error(flotes)
    return flotes

def flote_by_name(name):
    flotes = Flote.objects.filter(name=name)
    flotes = serializers.serialize('json', flotes)
    flotes = json.loads(flotes)
    logger.error(flotes[0])
    return flotes[0]