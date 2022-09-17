from django.db import models  
from django.forms import fields  
from polls.models import Flote, Image
from django import forms  
  
  
class FloteForm(forms.ModelForm):  
    class Meta:  
        # To specify the model to be used to create form  
        model = Flote
        # It includes all the fields of model  
        fields = '__all__'  

class ImageForm(forms.ModelForm):
    image = forms.ImageField(
        label="Image",
        widget=forms.ClearableFileInput(attrs={"multiple": True}),
    ) 

    class Meta:
        model = Image
        fields = ("image",)