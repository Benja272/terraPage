from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField


class Flote(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(primary_key=True, max_length=50)
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    patent = models.CharField(max_length=20)
    engine_n = models.IntegerField(null=True, blank=True)
    chassis_n = models.IntegerField(null=True, blank=True)
    production_year = models.DateField(null=True, blank=True)
    status = models.IntegerField(default=1)
    justifyStatus = models.CharField(max_length=300, blank=True, default="")
    operators = ArrayField(models.CharField(max_length=50, blank=True), default=[])
    views = ArrayField(models.ImageField(), blank=True, default=[])

    def __str__(self):
        return "%s %s" % (self.name, self.code)


class Repair(models.Model):
    type = models.IntegerField()
    date = models.DateField()
    mileage = models.IntegerField() #kilometraje
    description = models.CharField(max_length=300)
    cost = models.FloatField()
    flote = models.ForeignKey(Flote, on_delete=models.CASCADE)


    class Meta:
        ordering = ['date']

    def __str__(self):
        return "%s %s" % (self.date, self.flote.__str__())