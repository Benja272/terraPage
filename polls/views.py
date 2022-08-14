# Create your views here.
from django.http import JsonResponse, HttpRequest
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm

from django.contrib import messages
from django.shortcuts import render, redirect

from polls.sevices import flotes, flote_by_name

import logging
logger = logging.getLogger(__name__)
#Flote.objects.create(name="camionee", code="2131", brand="renault", patent="212adc", status=1)

def get_flote_by_name(request, name):
    flote = flote_by_name(name)
    return JsonResponse(flote)
    #return HttpResponse(f"<h1>Hello and welcome to my first <u>{name}</u> project!</h1>")

def get_flotes(request):
    flotes = flotes()
    return JsonResponse(flotes, safe=False)

def get_home_page(request):
    return render(request, 'ti_ingreso.html')

def get_flotes_page(request):
    return render(request, 'ti_vista-flota.html')


# auth
def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('ti_vista-flota.html')
        else:
            messages.success(request, "Usuario o Contraseña erroneos, por favor intente de nuevo.")
            return redirect('ti_ingreso.html')

def logout_user(request):
    logout(request)
    messages.success(request, ("Sesion cerrada."))
    return redirect('ti_ingreso.html')

def register_user(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request, "El usuario se registro exitosamente.")
            return redirect('ti_vista-flota.html')
    else:
        form = UserCreationForm()

        return render(request, 'ti_ingreso.html', {
            'form':form,
        })