from platform import mac_ver
from django.db import models

# Create your models here.
class Operator(models.Model):
    name = models.CharField(primary_key=True, default="",max_length=60)

    def __str__(self):
        return self.first_name


class Flote(models.Model):
    name = models.CharField(max_length=30)
    code = models.CharField(primary_key=True, max_length=30)
    brand = models.CharField(max_length=30)
    patent = models.CharField(max_length=20)
    engine_n = models.IntegerField()
    chassis_n = models.IntegerField()
    production_year = models.DateField()
    status = models.IntegerField()
    justifyStatus = models.CharField(max_length=300)
    operator = models.ForeignKey(Operator, default="", on_delete=models.PROTECT)

    def __str__(self):
        return "%s %s" % (self.name, self.code)


class Repair(models.Model):
    is_mantenance = models.BooleanField()
    date = models.DateField()
    mileage = models.IntegerField() #kilometraje
    description = models.CharField(max_length=300)
    cost = models.FloatField()
    flote = models.ForeignKey(Flote, on_delete=models.CASCADE)


    class Meta:
        ordering = ['date']

    def __str__(self):
        return "%s %s" % (self.date, self.flote.__str__())