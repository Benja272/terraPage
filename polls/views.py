# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from polls.forms import FloteForm, ImageForm, MaintenanceForm
from polls.sevices import flotes, flote_by_code, login_service
from polls.decorators import unauthenticated_user, allowed_users
from polls.models import Image, Flote
from datetime import datetime

import logging
logger = logging.getLogger(__name__)
#Flote.objects.create(name="camionee", code="2131", brand="renault", patent="212adc", status=1)

@login_required(login_url='/home/')
def get_flote_by_code(request, code):
    flote = flote_by_code(code)
    return render(request, 'flota.html', {'flote': flote})


@unauthenticated_user
def get_home_page(request):
    return render(request, 'ti_ingreso.html')


@login_required(login_url='/home/')
def get_flotes_page(request):
    json_flotes = flotes()
    logger.info(json_flotes)
    return render(request, 'ti_vista-flota.html', {'info': json_flotes})


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

@allowed_users(allowed_roles=['admin'])
def add_flote(request):
    if request.method == 'POST':
        form = FloteForm(request.POST, request.FILES)
        files = request.FILES.getlist("image")
        if form.is_valid():
            flote = form.save()
            # flote = Flote.objects.get(code=request.POST["code"])
            for image in files:
                Image.objects.create(flote=flote, image=image)
            messages.success(request, "Flota Agregada!")
            return redirect("/home/")
        else:
            print(form.errors)
    else:
        form = FloteForm()
        image_form = ImageForm()
        return render(request, 'add_flote.html', {'form': form, "imageform": image_form})

@allowed_users(allowed_roles=['admin'])
def add_repair(request, code):
    if request.method == 'POST':
        flote = Flote.objects.get(code=code)
        post = request.POST.copy()
        post['flote'] = flote.code
        post['date'] = datetime.now()
        form = MaintenanceForm(post)
        if form.is_valid() and flote:
            form.save()
            messages.success(request, "Se registro correctamente!")
            return redirect("/home/")
        else:
            print(form.errors)
    else:
        images = Image.objects.filter(flote__code = code)
        image_url = images[0].image.url if images else ""
        form = MaintenanceForm()
        fields = {"array": ['Tipo', 'Kilometraje', 'Descripción', 'Costo']}
        return render(request, 'add_maintenance.html',\
            {'form': form, 'image_url': image_url, "avoid_fields": fields})



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
