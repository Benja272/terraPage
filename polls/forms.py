from django.db import models  
from django.forms import fields , ModelForm , ClearableFileInput, ImageField
from django import forms 
from polls.models import Flote, Image, STATES, FLOTE_TYPES

FIELDS_TRANSLATE = {
    'type': 'Tipo',
    'code': 'Código',
    'brand': 'Marca',
    'model': 'Modelo',
    'characteristics': 'Caracteristicas',
    'patent': 'Patente',
    'production_year': 'Año de Producción',
    'engine_number': 'Numero de Motor',
    'chassis_number': 'Numero de Chassis',
    'status': 'Estado',
    'justifyStatus': 'Justificación del Estado',
    'operators': 'Operadores'
}

CSS_CLASS = {
    'type': {'class': 'card'},
    'code': {'class': 'card'},
    'brand': {'class': 'card'},
    'model': {'class': 'card'},
    'characteristics': {'class': 'card'},
    'patent': {'class': 'card'},
    'production_year': {'class': 'card'},
    'engine_number': {'class': 'card'},
    'chassis_number': {'class': 'card'},
    'status': {'class': 'card'},
    'justifyStatus': {'class': 'card'},
    'operators':{'class': 'card'} 
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
            'status': forms.Select(attrs=CSS_CLASS['status']),
        }

class ImageForm(ModelForm):
    image = ImageField(
        label="Fotos de la flota",
        widget=ClearableFileInput(attrs={"multiple": True}),
    ) 

    class Meta:
        model = Image
        fields = ("image",)