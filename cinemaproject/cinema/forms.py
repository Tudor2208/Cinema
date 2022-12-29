from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import *

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'duration', 'genre', 'director', 'release_date', 'description', 'link_trailer']

class ShowForm(forms.ModelForm):
    class Meta:
        model = Show
        fields = "__all__"

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = "__all__" 

class EmployeeForm(forms.ModelForm):
    class Meta: 
        model = Employee
        fields = "__all__"                 