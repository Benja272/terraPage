# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from polls.forms import FloteForm, ImageForm, MaintenanceForm, FloteForm2, ImageForm2
from polls.sevices import flotes, flote_by_code, login_service, maintenances, create_images\
    , generate_notifications
from polls.decorators import unauthenticated_user, allowed_users
from polls.models import Image, Flote, Maintenance
from datetime import date, datetime
from django.db.models import Q

import logging
logger = logging.getLogger(__name__)


@login_required(login_url='/home/')
def get_flote_by_code(request, code):
    flote, flote_in_db = flote_by_code(code)
    if request.method == 'POST':
        form = FloteForm2(request.POST, request.FILES, instance=flote_in_db)
        files = request.FILES.getlist("image")
        if form.is_valid():
            flote = form.save()
            create_images(flote, files)
            return redirect("/home/flotes/" + code)
        else:
            errors = ".".join(err[0] for err in form.errors.values())
            messages.error(request, errors)
            redirect("/flotes/add")
    else:
        correct_group = False
        if request.user.groups.all()[0].name == 'admin':
            correct_group = True
        if flote:
            update_form = FloteForm2(instance=flote_in_db)
            image_form = ImageForm2()
            notifications = generate_notifications(flote_in_db)
            return render(request, 'flota.html', {'flote': flote, "update_form": update_form,
                        "correct_group": correct_group, 'imageform': image_form, "notifications": notifications})
        else:
            messages.error(request, ("La flota no existe."))
            return redirect("/home/flotes")


@unauthenticated_user
def get_home_page(request):
    return render(request, 'ti_ingreso.html')


@login_required(login_url='/home/')
def get_flotes_page(request):
    if request.method == 'POST':
        print("/home/flotes/" + request.POST['code'])
        return redirect("/home/flotes/" + request.POST['code'])
    json_flotes = flotes()
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
            return redirect("/home/flotes/" + flote.code)
        else:
            errors = ".".join(err[0] for err in form.errors.values())
            messages.error(request, errors)
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
        form = MaintenanceForm(post)
        if form.is_valid() and flote and control_date(request, post):
            form.save()
            return redirect("/home/flotes/" + flote.code)
        else:
            errors = ".".join(err[0] for err in form.errors.values())
            messages.success(request, errors)
            return redirect("/home/flotes/add_repair/" + code)
    else:
        images = Image.objects.filter(flote__code=code)
        image_url = images[0].image.url if images else ""
        form = MaintenanceForm()
        fields = [field.label for field in form.fields.values()]
        fields = {"array": list(filter(lambda x: x != 'Flote', fields))}
        return render(request, 'add_maintenance.html',
                    {'form': form, 'image_url': image_url, "avoid_fields": fields, "code": code})

def control_date(request, post):
    res = datetime.strptime(post['date'], '%Y-%m-%d').date() <= date.today()
    if not res:
        messages.error(request, "La fecha debe ser menor que la actual.")

    return res


@login_required(login_url='/home/')
def list_repair(request, code):
    xs = maintenances(code)
    return render(request, 'maintenance_history.html', {'list': xs, 'code': code})


@allowed_users(allowed_roles=['admin'])
def delete_flote(request, code):
    flotes = Flote.objects.filter(code=code)
    if flotes:
        flotes.first().delete()
        messages.success(request, "Se elimino correctamente!")
    else:
        messages.error(request, "No existe la flota!")
    return redirect("/home/flotes/")


@allowed_users(allowed_roles=['admin'])
def delete_repair(request, pk):
    repairs = Maintenance.objects.filter(pk=pk)
    if repairs:
        repair = repairs.first()
        code = repair.flote.code
        repair.delete()
        messages.success(request, "Se elimino correctamente!")
        return redirect("/home/flotes/repair/" + code)
    else:
        messages.error(request, "No existe!")
        return redirect("/home/flotes")


@allowed_users(allowed_roles=['admin'])
def delete_img(request, pk):
    images = Image.objects.filter(pk=pk)
    if images:
        img = images.first()
        code = img.flote.code
        img.delete()
        messages.success(request, "Se elimino correctamente!")
        return redirect("/home/flotes/" + code)
    else:
        messages.error(request, "No existe la foto!")
        return redirect("/home/flotes")
