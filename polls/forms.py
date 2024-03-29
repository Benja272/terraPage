from ast import operator
from django.db import models
from django.forms import fields , ModelForm , ClearableFileInput, ImageField
from django import forms
from django.conf import settings
from polls.models import Alert, Flote, Maintenance, Image, STATES, FLOTE_TYPES

FIELDS_FLOTE_TRANSLATE = {
    'type': 'Tipo',
    'code': 'Código',
    'brand': 'Marca',
    'model': 'Modelo',
    'characteristics': 'Características',
    'patent': 'Patente',
    'production_year': 'Año de Fabricación',
    'engine_number': 'Número de Motor',
    'chassis_number': 'Número de Chasis',
    'status': 'Estado',
    'justifyStatus': 'Observaciones',
    'operators': 'Operadores'
}


FIELDS_MAINTENANCE_TRANSLATE = {
    'type': 'Tipo',
    'mileage': 'Kilometraje',
    'cost': 'Costo',
    'description': 'Descripción',
    'oil': 'Cambio de aceite',
    'filter': 'Cambio de filtro',
    'date': 'Fecha'
}

FIELDS_ALERTS_TRANSLATE = {
    'flote': 'Flota',
    'limit_date': 'Fecha límite',
    'title': 'Título',
    'description': 'Descripción',
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
    'status': {'class': 'form-select', 'id': 'status'},
    'justifyStatus': {'class': 'form-control'},
    'operators':{'class': 'form-control'} 
}

CSS_FLOTE_CLASS2 = {
    'type': {'class': 'form-select text-center', "disabled":""}, 
    'code': {'class': 'form-control text-center', "disabled":""},
    'brand': {'class': 'form-control text-center', "disabled":""},
    'model': {'class': 'form-control text-center', "disabled":""},
    'characteristics': {'class': 'form-control text-center', "disabled":""},
    'patent': {'class': 'form-control text-center', "disabled":""},
    'production_year': {'class': 'form-control text-center', "disabled":""},
    'engine_number': {'class': 'form-control text-center', "disabled":""},
    'chassis_number': {'class': 'form-control text-center', "disabled":""},
    'status': {'class': 'form-select text-center', "disabled":"", 'id': 'status'},
    'justifyStatus': {'class': 'form-control text-center', "disabled":""},
    'operators':{'class': 'form-control text-center', "disabled":""} 
}



CSS_MAINTENANCE_CLASS = {
    'flote': {'type': 'hidden'},
    'date': {'type': 'date', 'class':'form-control'},
    'type': {'class': 'form-select'},
    'mileage': {'class': 'form-control'},
    'cost': {'class': 'form-control'},
    'description': {'class': 'form-control'},
    'oil': {'class': 'form-check-input','type': 'checkbox', 'id': 'flexCheckDefault'},
    'filter': {'class': 'form-check-input', 'type': 'checkbox', 'id': 'flexCheckDefault'}
}



CSS_ALERT_CLASS = {
    'flote': {'class': 'form-select text-center'},
    'limit_date': {'type': 'date', 'class':'form-control'},
    'title': {'class': 'form-control'},
    'description': {'class': 'form-control'}
}



class FloteForm(ModelForm):
    class Meta:
        model = Flote
        fields = ['type', 'code', 'brand', 'model', 'patent', 'production_year', 'engine_number', 'chassis_number', 'characteristics', 'status', 'justifyStatus', 'operators']
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
            'engine_number': forms.TextInput(attrs=CSS_FLOTE_CLASS['engine_number']),
            'chassis_number': forms.TextInput(attrs=CSS_FLOTE_CLASS['chassis_number']),
            'status': forms.Select(attrs=CSS_FLOTE_CLASS['status']),
            'justifyStatus': forms.TextInput(attrs=CSS_FLOTE_CLASS['justifyStatus']),
            'operators' : forms.TextInput(attrs=CSS_FLOTE_CLASS['operators'])
        }

# flota
class FloteForm2(ModelForm):
    class Meta:
        model = Flote
        fields = ['type', 'code', 'brand', 'model', 'patent', 'production_year', 'engine_number', 'chassis_number', 'characteristics', 'status', 'justifyStatus', 'operators']
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
            'engine_number': forms.TextInput(attrs=CSS_FLOTE_CLASS2['engine_number']),
            'chassis_number': forms.TextInput(attrs=CSS_FLOTE_CLASS2['chassis_number']),
            'status': forms.Select(attrs=CSS_FLOTE_CLASS2['status']),
            'justifyStatus': forms.TextInput(attrs=CSS_FLOTE_CLASS2['justifyStatus']),
            'operators': forms.TextInput(attrs=CSS_FLOTE_CLASS2['operators'])
        }

class ImageForm(ModelForm):
    image = ImageField(
        label="Fotos de la flota",
        widget=ClearableFileInput(attrs={"multiple": True, "class": "form-control"}),
    )

    class Meta:
        model = Image
        fields = ("image",)

    def __init__(self, *args, **kwargs):
        super(ImageForm, self).__init__(*args, **kwargs)
        self.fields['image'].required = False

class ImageForm2(ModelForm):
    image = ImageField(
        label="Fotos de la flota",
        widget=ClearableFileInput(attrs={"multiple": True, "class": "form-control", "disabled":""}),
    )

    class Meta:
        model = Image
        fields = ("image",)

    def __init__(self, *args, **kwargs):
        super(ImageForm2, self).__init__(*args, **kwargs)
        self.fields['image'].required = False

class MaintenanceForm(ModelForm):
    class Meta:
        model = Maintenance
        fields = ['flote', 'date', 'type','mileage','cost', 'description', 'oil', 'filter']
        labels = FIELDS_MAINTENANCE_TRANSLATE
        widgets = {
            'flote': forms.DateInput(attrs=CSS_MAINTENANCE_CLASS['flote']),
            'date': forms.DateInput(format='%d %B, %Y', attrs=CSS_MAINTENANCE_CLASS['date']),
            'type': forms.Select(attrs=CSS_MAINTENANCE_CLASS['type']),
            'mileage': forms.NumberInput(attrs=CSS_MAINTENANCE_CLASS['mileage']),
            'cost': forms.NumberInput(attrs=CSS_MAINTENANCE_CLASS['cost']),
            'description': forms.TextInput(attrs=CSS_MAINTENANCE_CLASS['description']),
            'oil': forms.CheckboxInput(attrs=CSS_MAINTENANCE_CLASS['oil']),
            'filter': forms.CheckboxInput(attrs=CSS_MAINTENANCE_CLASS['filter'])
        }

class AlertForm(ModelForm):
    class Meta:
        model = Alert
        fields = ['flote', 'limit_date', 'title', 'description']
        labels = FIELDS_ALERTS_TRANSLATE
        # limit_date = forms.DateField(input_formats= '%Y-%m-%d' , widget=forms.DateInput(format='%Y-%m-%d' ,attrs=CSS_ALERT_CLASS['limit_date']))
        widgets = {
            'flote' : forms.Select(attrs=CSS_ALERT_CLASS['flote']),
            'limit_date': forms.DateInput(format='%d %B, %Y', attrs=CSS_ALERT_CLASS['limit_date']),
            'description': forms.TextInput(attrs=CSS_ALERT_CLASS['description']),
            'title': forms.DateInput(attrs=CSS_ALERT_CLASS['title'])
        }