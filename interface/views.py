from django.shortcuts import render
from django.http import HttpResponse


def dashboard(request):
    return render(request, 'interface/index.html')

def login_form(request):
    return render(request, 'interface/login.html')

def signup_form(request):
    return render(request, 'interface/signup.html')