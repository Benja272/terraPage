from distutils.command.build_scripts import first_line_re
from lib2to3.pgen2.token import OP
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import Operator

op = Operator(name="pedro")
op.save()

def index(request):
    return HttpResponse("<h1>Hello and welcome to my first <u>Django App</u> project!</h1>")

