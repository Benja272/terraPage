from django.db import models  
from django.forms import fields , ModelForm , ClearableFileInput, ImageField
from django import forms 
from polls.models import Flote, Image, STATES, FLOTE_TYPES

FIELDS_TRANSLATE = {
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

CSS_CLASS = {
    'type': {'class': 'form-select',},
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
    'operators':{'class': 'form-control'} 
}
  
class FloteForm(ModelForm):
    class Meta:
        model = Flote
        fields = '__all__'
        labels = FIELDS_TRANSLATE
        status = forms.ChoiceField(choices=STATES)
        type = forms.ChoiceField(choices=FLOTE_TYPES)

        widgets = {
            'type': forms.Select(attrs=CSS_CLASS['type']),
            'code': forms.TextInput(attrs=CSS_CLASS['code']),
            'brand': forms.TextInput(attrs=CSS_CLASS['brand']),
            'model': forms.TextInput(attrs=CSS_CLASS['model']),
            'characteristics': forms.TextInput(attrs=CSS_CLASS['characteristics']),
            'patent': forms.TextInput(attrs=CSS_CLASS['patent']),
            'production_year': forms.NumberInput(attrs=CSS_CLASS['production_year']),
            'engine_number': forms.NumberInput(attrs=CSS_CLASS['engine_number']),
            'chassis_number': forms.NumberInput(attrs=CSS_CLASS['chassis_number']),
            'status': forms.Select(attrs=CSS_CLASS['status']),
            'justifyStatus': forms.TextInput(attrs=CSS_CLASS['justifyStatus']),
            'operators': forms.TextInput(attrs=CSS_CLASS['operators']),
        }

class ImageForm(ModelForm):
    image = ImageField(
        label="Fotos de la flota",
        widget=ClearableFileInput(attrs={"multiple": True, "class": "form-control"}),
    ) 

    class Meta:
        model = Image
        fields = ("image",)