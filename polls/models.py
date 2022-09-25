from email.mime import image
from tokenize import blank_re
from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

STATES = [
    ('GRE', 'GREEN'),
    ('YEL', 'YELLOW'),
    ('RED', 'RED')
]

FLOTE_TYPES = [
    ('CAM', 'CAMIONETA'),
    ('RET', 'RETROESCAVADORA'),
    ('CAR', 'CARRETON'),
    ('MOT', 'MOTONIVELADORA'),
    ('CAO', 'CAMIÓN'),
    ('TAN', 'TANQUE DE COMBUSTIBLE'),
]

class Flote(models.Model):
    type = models.CharField(choices=FLOTE_TYPES, max_length=50)
    code = models.CharField(primary_key=True, max_length=50)
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    characteristics = models.CharField(max_length=600, blank=True)
    patent = models.CharField(max_length=20, blank=True)
    production_year = models.DateField(null=True, blank=True)
    engine_number = models.IntegerField(null=True, blank=True)
    chassis_number = models.IntegerField(null=True, blank=True)
    status = models.CharField(choices=STATES, max_length=30)
    justifyStatus = models.CharField(max_length=600, blank=True, default="")
    operators = ArrayField(models.CharField(max_length=50, blank=True), default=list)

    def __str__(self):
        return "%s %s %s" % (self.type, self.code, self.status)

MAINTENANCE_TYPES = [
    ('REP', 'REPAIR'),
    ('MAN', 'MAINTENANCE')
]
class Maintenance(models.Model):
    type = models.CharField(choices=MAINTENANCE_TYPES, max_length=30)
    date = models.DateField()
    mileage = models.IntegerField() #kilometraje
    description = models.CharField(max_length=600)
    cost = models.FloatField()
    flote = models.ForeignKey(Flote, on_delete=models.CASCADE)


    class Meta:
        ordering = ['date']

    def __str__(self):
        return "%s %s" % (self.type, self.date, self.flote.__str__())


class Image(models.Model):
    flote = models.ForeignKey(Flote, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', null=True, blank=True)