# Create your views here.
from django.http import JsonResponse, HttpRequest
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.shortcuts import render, redirect
from polls.forms import FloteForm
from polls.sevices import flotes, flote_by_name, flote_create, login_service
from polls.decorators import unauthenticated_user, allowed_users
from polls.models import Flote

import logging
logger = logging.getLogger(__name__)
#Flote.objects.create(name="camionee", code="2131", brand="renault", patent="212adc", status=1)


def get_flote_by_name(request, name):
    flote = flote_by_name(name)
    return JsonResponse(flote)


@unauthenticated_user
def get_home_page(request):
    return render(request, 'ti_ingreso.html')


@login_required(login_url='/home/')
def get_flotes_page(request):
    json_flotes = flotes()
    logger.info(json_flotes)
    return render(request, 'ti_vista-flota.html', {'flotes': json_flotes})


@allowed_users(allowed_roles=['admin'])
def create_flote(request):
    if request.method == "POST":
        flote_create(request)

# auth


@unauthenticated_user
def login_user(request):
    logger.info(request)
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        redirect_url = login_service(request, username, password)
        return redirect(redirect_url)


@login_required(login_url='/home/')
def logout_user(request):
    logger.error(request.user)
    logout(request)
    messages.success(request, ("Sesion cerrada."))
    return redirect('/home/')


def add_flote(request):
    if request.method == 'POST':
        form = FloteForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

            # Getting the current instance object to display in the template
            img_object = form.instance

            return render(request, 'add_flote.html', {'form': form, 'img_obj': img_object})
    else:
        form = FloteForm()

    return render(request, 'add_flote.html', {'form': form})


# def register_user(request):
#     if request.method == "POST":
#         username = ""
#         password1 = ""
#         password2 = ""
#         form = UserCreationForm(username, password1, password2)
#         redirect_url = '/home/'
#         if form.is_valid():
#             form.save()
#             messages.success(request, "El usuario se registro exitosamente.")
#             redirect_url = login_service(request, username, password1)

#         return redirect(redirect_url)
