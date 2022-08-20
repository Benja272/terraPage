# Create your views here.
from django.http import JsonResponse, HttpRequest
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.shortcuts import render, redirect

from polls.sevices import flotes, flote_by_name
from polls.decorators import unauthenticated_user
from polls.models import Flote

import logging
logger = logging.getLogger(__name__)
#Flote.objects.create(name="camionee", code="2131", brand="renault", patent="212adc", status=1)

def get_flote_by_name(request, name):
    flote = flote_by_name(name)
    return JsonResponse(flote)
    #return HttpResponse(f"<h1>Hello and welcome to my first <u>{name}</u> project!</h1>")

def get_flotes(request):
    json_flotes = flotes()
    return JsonResponse(flotes, safe=False)

@unauthenticated_user
def get_home_page(request):
    return render(request, 'ti_ingreso.html')

@login_required(redirect_field_name='home')
def get_flotes_page(request):
    json_flotes = flotes()
    logger.info(json_flotes)
    return render(request, 'ti_vista-flota.html', {'flotes': json_flotes})


# auth
def login_service(request, username, password):
    user = authenticate(request, username=username, password=password)
    redirect_url = 'home/flotes'
    if user:
        login(request, user)
    else:
        messages.success(request, "Usuario o Contraseña erroneos, por favor intente de nuevo.")
        redirect_url = 'home/'
    return redirect_url

def login_user(request):
    logger.info(request)
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        redirect_url = login_service(request, username, password)
        return redirect(redirect_url)

def logout_user(request):
    logout(request)
    messages.success(request, ("Sesion cerrada."))
    return redirect('home/')

def register_user(request):
    if request.method == "POST":
        username = ""
        password1 = ""
        password2 = ""
        form = UserCreationForm(username, password1, password2)
        redirect_url = 'home/'
        if form.is_valid():
            form.save()
            messages.success(request, "El usuario se registro exitosamente.")
            redirect_url = login_service(request, username, password1)

        return redirect(redirect_url)
