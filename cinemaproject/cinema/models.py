from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Message(models.Model):
    sender = models.CharField(max_length=30)
    text = models.CharField(max_length=250)
    send_date = models.DateField(auto_now_add=True, auto_now=False)
    response = models.CharField(max_length=250, default = "none")
 
class Genre(models.Model):
    name = models.CharField(max_length=50)
 
    def __str__(self):
        return self.name
 
class Movie(models.Model):
    title = models.CharField(max_length=200)
    duration = models.IntegerField()
    genre = models.ManyToManyField(Genre)
    director = models.CharField(max_length=200)
    release_date = models.DateField()
    description = models.TextField(max_length=1000)
    link_trailer = models.CharField(max_length=300, null=True)

    def __str__(self):
        return self.title
 
class Show(models.Model):
    movie_ID = models.ForeignKey('Movie', on_delete=models.SET_NULL, null=True)
    cinema_hall_ID = models.ForeignKey(
        'CinemaHall', on_delete=models.SET_NULL, null=True)
    date = models.DateField()
    start_hour = models.TimeField()
    end_hour = models.TimeField()
    view_mode = models.CharField(max_length=45)
 
    def __str__(self):
        return str(self.movie_ID) + " / " + str(self.date) + " / " + str(self.start_hour)
 
class CinemaHall(models.Model):
    nr_of_seats = models.IntegerField()
    accept_4DX = models.BooleanField()
 
    def __str__(self):
        return str(self.nr_of_seats) + " " + str(self.accept_4DX)
 
class Employee(models.Model):
    salary = models.FloatField()
    user_id = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return str(self.user_id) + " " + str(self.salary)    
 
class Admin(models.Model):
    user_id = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True)
 
class ShowSeat(models.Model):
    show_ID = models.ForeignKey('Show', on_delete=models.SET_NULL, null=True)
    booking_ID = models.ForeignKey(
        'Booking', on_delete=models.SET_NULL, null=True)
    seat_nr = models.IntegerField()
    booked = models.BooleanField(default = False)

    def __str__(self):
        return str(self.show_ID) + " " + str(self.seat_nr) + " " + str(self.booked)  
 
class Ticket(models.Model):
    category = models.CharField(max_length=20)
    price = models.FloatField()
    
    def __str__(self):
        return str(self.category) + " - " + str(self.price) + " lei"

class Booking(models.Model):
    show_id = models.ForeignKey('Show', on_delete=models.SET_NULL, null=True)
    user_id = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True)
    nr_of_seats = models.IntegerField()
    booking_time = models.TimeField()
    total_price = models.FloatField()

    def __str__(self):
        return str(self.show_id) + " " + str(self.user_id) + " " + str(self.nr_of_seats) + " " + str(self.booking_time)     