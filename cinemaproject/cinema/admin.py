from django.contrib import admin
# Register your models here.

from .models import *
 

admin.site.register(Genre)
admin.site.register(Admin)
admin.site.register(Movie)
admin.site.register(Show)
admin.site.register(Employee)
admin.site.register(CinemaHall)
admin.site.register(Ticket)
admin.site.register(Booking)
admin.site.register(ShowSeat)
admin.site.register(Message)
admin.site.register(Notification)
admin.site.register(SiteSettings)