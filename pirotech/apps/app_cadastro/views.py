from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def login(request):
    return render(request,'app_cadastro/login.html')

def cadastro(request):
    return render(request,'app_cadastro/cadastro.html')

def cadastro_home(request):
    return render(request,'app_cadastro/home.html')
