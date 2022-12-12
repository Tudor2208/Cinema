from django.urls import path
from . import views

urlpatterns = [
    path("index", views.index, name="index"),
    path("login", views.loginPage, name="login"),
    path("logout", views.logoutPage, name="logout"),
    path("profile", views.profilePage, name="profile"),
    path("register", views.register, name="register"),
    path("employee", views.employeePage, name="employee"),
    path("admin", views.adminPage, name="admin")
]