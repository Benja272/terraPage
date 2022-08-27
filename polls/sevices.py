import json
from django.core import serializers
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

def to_json(entities):
    if entities:
        entities = serializers.serialize('json', entities)
        entities = json.loads(entities)
    return entities
    