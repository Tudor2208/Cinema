from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import *
from django.utils import timezone
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
    view_mode = models.CharField(max_length=45)
 
    def __str__(self):
        return str(self.movie_ID) + " / " + str(self.date) + " / " + str(self.start_hour) + " / " + str(self.view_mode)
 
class CinemaHall(models.Model):
    nr_of_seats = models.IntegerField()
    accept_4DX = models.BooleanField()

    def __str__(self):
        if self.accept_4DX:
            return "S" + str(self.id) + " (" + str(self.nr_of_seats) + " locuri, 4DX)"
        return "S" + str(self.id) + " (" + str(self.nr_of_seats) + " locuri)"     
 
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
        return str(self.show_ID) + " / locul " + str(self.seat_nr) + " - " + str(self.booked)  
 
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
        return str(self.show_id) + " / " + str(self.user_id) + " / " + str(self.nr_of_seats) + " / " + str(self.booking_time) + " / " + str(self.total_price) + " lei"    

class Notification(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    text = models.CharField(max_length=300)
    time = models.TimeField(default=timezone.now)
    sent_date = models.DateField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return "Ptr " + str(self.user_id) + ": " + self.text + " (" + str(self.sent_date) + ")"

class SingletonModel(models.Model):

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super(SingletonModel, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class SiteSettings(SingletonModel):
    site_name = models.CharField(max_length=255, default='CinemaCity')
    bookings_status = models.BooleanField(default=True) # enabled / disabled
    contact_status = models.BooleanField(default=True)

    def __str__(self):
        return self.site_name + ", bilete: " + str(self.bookings_status) + ", contact: " + str(self.contact_status)

@receiver(post_save, sender=Show)
def hear_signal(sender, instance, **kwargs):
    if kwargs.get('created'):
        cinema_hall = CinemaHall.objects.filter(id=instance.cinema_hall_ID.id)[0]
        mock_booking = Booking.objects.filter(id=4)[0]
        seats = cinema_hall.nr_of_seats
        for i in range(seats):
            #booking 4 - e hardcodat, inseamna NULL
            showSeat = ShowSeat(show_ID=instance, booking_ID=mock_booking, seat_nr=i+1, booked=False)
            showSeat.save()   
    return

@receiver(post_save, sender=Message)
def hear_signal_message(sender, instance, **kwargs):
    if not kwargs.get('created'):
        user = User.objects.get(username=instance.sender)
        Notification(user_id=user, text="Un angajat tocmai ti-a raspuns la un mesaj!").save()

    return

    #TODO: de adaugat mai multe tipuri de notificari


@receiver(post_save, sender=Employee)
def hear_signal_employee(sender, instance, **kwargs):
    if kwargs.get('created'):
        user = User.objects.get(username=instance.user_id)
        role = Group.objects.get(name = 'employee')
        is_admin = User.objects.filter(username=instance.user_id, groups__name='admin').exists()
        if not is_admin:
            role.user_set.add(user)
        employees = Employee.objects.filter(user_id=instance.user_id)
        
        if len(employees) > 1:
            employees[0].delete()
            Notification(user_id=user, text="Salariul ți-a fost actualizat! Noul salariu: " + str(employees[1].salary) + " lei").save()    
        else:
            Notification(user_id=user, text="Salariul ți-a fost actualizat! Noul salariu: " + str(employees[0].salary) + " lei").save()    

@receiver(pre_delete, sender=Employee)
def hear_signal_del_employee(sender, instance, **kwargs):
    user = instance.user_id
    Notification(user_id=user, text="Ai fost concediat!").save()
    group = Group.objects.get(name='employee') 
    user.groups.remove(group)
