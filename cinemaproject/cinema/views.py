from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from .decorators import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.


def index(request):
    return render(request, 'cinema/Homepage.html')

def profilePage(request):
    if not request.user.is_authenticated:
        return redirect('login')

    return render(request, 'cinema/Profile.html')

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate (request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.info(request, "Numele de utilizator sau parola sunt gresite!")

    return render(request, 'cinema/Login.html')

@login_required(login_url = "login")
def logoutPage(request):
    logout(request)
    return redirect('login')

def register(request):
    if request.user.is_authenticated:
        return redirect('index')

    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Contul a fost creat cu succes!")
            return redirect('login')

    context = {'form' : form}
    return render(request, 'cinema/Register.html', context)

@allowed_users(allowed_roles=['employee', 'admin'])
def employeePage(request):
    return render(request, 'cinema/Employee.html')

@allowed_users(allowed_roles=['admin'])
def adminPage(request):
    return render(request, 'cinema/Admin.html')
   

