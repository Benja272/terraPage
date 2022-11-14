from ast import operator
from django.db import models  
from django.forms import fields , ModelForm , ClearableFileInput, ImageField
from django import forms 
from django.contrib.postgres.forms import SimpleArrayField
from polls.models import Flote, Maintenance, Image, STATES, FLOTE_TYPES

FIELDS_FLOTE_TRANSLATE = {
    'type': 'Tipo',
    'code': 'Código',
    'brand': 'Marca',
    'model': 'Modelo',
    'characteristics': 'Características',
    'patent': 'Patente',
    'production_year': 'Año de Producción',
    'engine_number': 'Número de Motor',
    'chassis_number': 'Número de Chasis',
    'status': 'Estado',
    'justifyStatus': 'Justificación del Estado',
    'operators': 'Operadores'
}


FIELDS_MAINTENANCE_TRANSLATE = {
    'type': 'Tipo',
    'mileage': 'Kilometraje',
    'cost': 'Costo',
    'description': 'Descripción'
}

CSS_FLOTE_CLASS = {
    'type': {'class': 'form-select'},
    'code': {'class': 'form-control'},
    'brand': {'class': 'form-control'},
    'model': {'class': 'form-control'},
    'characteristics': {'class': 'form-control'},
    'patent': {'class': 'form-control'},
    'production_year': {'class': 'form-control'},
    'engine_number': {'class': 'form-control'},
    'chassis_number': {'class': 'form-control'},
    'status': {'class': 'form-select'},
    'justifyStatus': {'class': 'form-control'},
    'operators':{'class': 'form-control', 'placeholder' : 'Ingresar nombres separados por comas'} 
}

CSS_FLOTE_CLASS2 = {
    'type': {'class': 'form-select', "disabled":""},
    'code': {'class': 'form-control'},
    'brand': {'class': 'form-control'},
    'model': {'class': 'form-control'},
    'characteristics': {'class': 'form-control'},
    'patent': {'class': 'form-control'},
    'production_year': {'class': 'form-control'},
    'engine_number': {'class': 'form-control'},
    'chassis_number': {'class': 'form-control'},
    'status': {'class': 'form-select'},
    'justifyStatus': {'class': 'form-control'},
    'operators':{'class': 'form-control', 'placeholder' : 'Ingresar nombres separados por comas'} 
}



CSS_MAINTENANCE_CLASS = {
    'flote': {'type': 'hidden'},
    'date': {'type': 'hidden'},
    'type': {'class': 'form-select'},
    'mileage': {'class': 'form-control'},
    'cost': {'class': 'form-control'},
    'description': {'class': 'form-control'}
}
  
class FloteForm(ModelForm):
    class Meta:
        model = Flote
        fields = '__all__'
        labels = FIELDS_FLOTE_TRANSLATE
        status = forms.ChoiceField(choices=STATES)
        type = forms.ChoiceField(choices=FLOTE_TYPES)

        widgets = {
            'type': forms.Select(attrs=CSS_FLOTE_CLASS['type']),
            'code': forms.TextInput(attrs=CSS_FLOTE_CLASS['code']),
            'brand': forms.TextInput(attrs=CSS_FLOTE_CLASS['brand']),
            'model': forms.TextInput(attrs=CSS_FLOTE_CLASS['model']),
            'characteristics': forms.TextInput(attrs=CSS_FLOTE_CLASS['characteristics']),
            'patent': forms.TextInput(attrs=CSS_FLOTE_CLASS['patent']),
            'production_year': forms.NumberInput(attrs=CSS_FLOTE_CLASS['production_year']),
            'engine_number': forms.NumberInput(attrs=CSS_FLOTE_CLASS['engine_number']),
            'chassis_number': forms.NumberInput(attrs=CSS_FLOTE_CLASS['chassis_number']),
            'status': forms.Select(attrs=CSS_FLOTE_CLASS['status']),
            'justifyStatus': forms.TextInput(attrs=CSS_FLOTE_CLASS['justifyStatus']),
            'operators' : forms.TextInput(attrs=CSS_FLOTE_CLASS['operators'])
        }

# flota
class FloteForm2(ModelForm):
    class Meta:
        model = Flote
        fields = '__all__'
        labels = FIELDS_FLOTE_TRANSLATE
        status = forms.ChoiceField(choices=STATES)
        type = forms.ChoiceField(choices=FLOTE_TYPES)

        widgets = {
            'type': forms.Select(attrs=CSS_FLOTE_CLASS2['type']),
            'code': forms.TextInput(attrs=CSS_FLOTE_CLASS2['code']),
            'brand': forms.TextInput(attrs=CSS_FLOTE_CLASS2['brand']),
            'model': forms.TextInput(attrs=CSS_FLOTE_CLASS2['model']),
            'characteristics': forms.TextInput(attrs=CSS_FLOTE_CLASS2['characteristics']),
            'patent': forms.TextInput(attrs=CSS_FLOTE_CLASS2['patent']),
            'production_year': forms.NumberInput(attrs=CSS_FLOTE_CLASS2['production_year']),
            'engine_number': forms.NumberInput(attrs=CSS_FLOTE_CLASS2['engine_number']),
            'chassis_number': forms.NumberInput(attrs=CSS_FLOTE_CLASS2['chassis_number']),
            'status': forms.Select(attrs=CSS_FLOTE_CLASS2['status']),
            'justifyStatus': forms.TextInput(attrs=CSS_FLOTE_CLASS2['justifyStatus']),
            'operators' : forms.TextInput(attrs=CSS_FLOTE_CLASS2['operators'])
        }

class ImageForm(ModelForm):
    image = ImageField(
        label="Fotos de la flota",
        widget=ClearableFileInput(attrs={"multiple": True, "class": "form-control"}),
    ) 

    class Meta:
        model = Image
        fields = ("image",)

class MaintenanceForm(ModelForm):
    
    class Meta:
        model = Maintenance
        fields = ['flote', 'date','type','mileage','cost', 'description']
        labels = FIELDS_MAINTENANCE_TRANSLATE
        widgets = {
            'flote': forms.DateInput(attrs=CSS_MAINTENANCE_CLASS['flote']),
            'date': forms.DateInput(attrs=CSS_MAINTENANCE_CLASS['date']),
            'type': forms.Select(attrs=CSS_MAINTENANCE_CLASS['type']),
            'mileage': forms.NumberInput(attrs=CSS_MAINTENANCE_CLASS['mileage']),
            'cost': forms.NumberInput(attrs=CSS_MAINTENANCE_CLASS['cost']),
            'description': forms.DateInput(attrs=CSS_MAINTENANCE_CLASS['description'])
        }
