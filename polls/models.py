from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.contrib.postgres.fields import ArrayField



STATES = [ # se puede modificar desde aca el css de STATES?
    ('GRE', 'VERDE'),
    ('YEL', 'AMARILLO'),
    ('RED', 'ROJO')
]

FLOTE_TYPES = [
    ('CAM', 'CAMIONETA'),
    ('RET', 'RETROESCAVADORA'),
    ('CAR', 'CARRETÓN'),
    ('MOT', 'MOTONIVELADORA'),
    ('CAO', 'CAMIÓN'),
    ('TAN', 'TANQUE DE COMBUSTIBLE'),
    ('TAR', 'TANQUE REGADOR'),
]

class Flote(models.Model):
    type = models.CharField(choices=FLOTE_TYPES, max_length=50)
    code = models.CharField(primary_key=True, max_length=50)
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    characteristics = models.CharField(max_length=600, blank=True)
    patent = models.CharField(max_length=20, blank=True)
    production_year = models.IntegerField(null=True, blank=True)
    engine_number = models.IntegerField(null=True, blank=True)
    chassis_number = models.IntegerField(null=True, blank=True)
    status = models.CharField(choices=STATES, max_length=30)
    justifyStatus = models.CharField(max_length=600, blank=True, default="")
    operators = ArrayField(models.CharField(max_length=50, blank=True), blank=True, default=list)

    def __str__(self):
        return "%s %s" % (self.code, self.brand)

MAINTENANCE_TYPES = [
    ('REP', 'REPARACIÓN'),
    ('MAN', 'MANTENIMIENTO')
]
class Maintenance(models.Model):
    type = models.CharField(choices=MAINTENANCE_TYPES, max_length=30)
    date = models.DateField(null=True, blank=True)
    mileage = models.IntegerField()
    description = models.CharField(max_length=600)
    cost = models.FloatField()
    flote = models.ForeignKey(Flote, on_delete=models.CASCADE, null=True, blank=True)


    class Meta:
        ordering = ['date']

    def __str__(self):
        return "%s %s" % (self.type, self.flote.__str__())


class Image(models.Model):
    flote = models.ForeignKey(Flote, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', null=True, blank=True)


