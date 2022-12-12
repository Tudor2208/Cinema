from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from .decorators import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
# Create your views here.


def index(request):
    return render(request, 'cinema/Homepage.html')

def profilePage(request): 
    if not request.user.is_authenticated:
        return redirect('login')
        
    if request.method == "POST":
        username = request.POST.get('username')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')

        if username != None:
            record = User.objects.get(username = request.user)
            record.username = username
            record.save(update_fields=['username'])

        if email != None:
            record = User.objects.get(username = request.user)
            record.email = email
            record.save(update_fields=['email'])

        if firstname != None:
            record = User.objects.get(username = request.user)
            record.first_name = firstname
            record.save(update_fields=['first_name'])

        if lastname != None:
            record = User.objects.get(username = request.user)
            record.last_name = lastname
            record.save(update_fields=['last_name'])

    context = {'user':request.user, 
               'email':request.user.email,
               'last_name':request.user.last_name,
               'first_name':request.user.first_name,
               'last_login':request.user.last_login,
               'date_joined':request.user.date_joined}
               

    return render(request, 'cinema/Profile.html', context=context)

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
   

