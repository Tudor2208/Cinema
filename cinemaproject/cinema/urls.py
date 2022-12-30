from django.urls import path
from . import views

urlpatterns = [
    path("index", views.index, name="index"),
    path("login", views.loginPage, name="login"),
    path("logout", views.logoutPage, name="logout"),
    path("profile", views.profilePage, name="profile"),
    path("register", views.register, name="register"),
    path("employee", views.employeePage, name="employee"),
    path("admin", views.adminPage, name="admin"),
    path("contact", views.contactPage, name="contact"),
    path("delete/message/<int:msg_nr>", views.deleteMessagePage, name ="delete_message"),
    path("schedule", views.schedulePage, name = "schedule"),
    path("create-movie", views.createMoviePage, name = "create_movie"),
    path("create-show", views.createShowPage, name = "create_show"),
    path("buyticket<int:show_nr>", views.ticketPage, name = "ticket"),
    path("selectseats<str:show_booking>", views.selectSeatsPage, name="seats"),
    path("success", views.successPage, name="success"),
    path("notifications", views.notificationPage, name="notification"),
    path("delete/notification/<int:notif_nr>", views.deleteNotificationPage, name ="delete_notification"),
    path("view-clients", views.viewClients, name="clients"),
    path("add-employee", views.addEmployee, name="add-employee"),
    path("modify-price", views.modifyPrice, name="modify-price"),
    path("view-statistics", views.viewStatistics, name="view-statistics"),
    path("delete/employee/<int:employee_id>", views.deleteEmployeePage, name ="delete_employee")
]