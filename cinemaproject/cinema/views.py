from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm, MovieForm, ShowForm, BookingForm, EmployeeForm
from .decorators import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from .models import Message, Show, ShowSeat, Ticket, Booking, Notification, Employee, SiteSettings
import pendulum
from datetime import date, datetime
import calendar
from django.urls import reverse
from fpdf import FPDF
from django.utils import timezone
# Create your views here.

def has_notif(context, request):
    context['settings'] = SiteSettings.load()
    context['has_notif'] = Notification.objects.filter(user_id=request.user).count() > 0

def index(request):
    context={}
    if request.user.is_authenticated:
        has_notif(context, request)
    return render(request, 'cinema/Homepage.html', context=context)

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

    salary = -1
    empl = Employee.objects.filter(user_id=request.user)
    if len(empl) > 0:
        salary = empl[0].salary

    context = {'user':request.user, 
               'email':request.user.email,
               'last_name':request.user.last_name,
               'first_name':request.user.first_name,
               'last_login':request.user.last_login,
               'date_joined':request.user.date_joined,
               'password': request.user.password,
               'salary' : salary}
               
    has_notif(context, request)
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

    context = {'settings':SiteSettings.load()}
    return render(request, 'cinema/Login.html', context=context)

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

    context = {'form' : form, 'settings':SiteSettings.load()}
    return render(request, 'cinema/Register.html', context)

@allowed_users(allowed_roles=['employee', 'admin'])
def employeePage(request):
    if request.method == "POST":
        resp = request.POST.get('response')
        id = request.POST.get('aux_field')
        msg = Message.objects.get(id = id)
        msg.response = resp
        msg.save(update_fields=['response'])

    all_messages = Message.objects.all()
    context = {'messages_list' : all_messages}
    has_notif(context, request)
    return render(request, 'cinema/Employee.html', context=context)

@allowed_users(allowed_roles=['admin'])
def adminPage(request):
    if request.method == 'POST':
        settings = SiteSettings.load()
        name = request.POST.get('modify-name')
        check1 = request.POST.get("check1")
        check2 = request.POST.get("check2")
    
        if check1 == "not_checked":
            settings.bookings_status = False
        elif check1 == "checked":
            settings.bookings_status = True
        elif check2 == "not_checked":
            settings.contact_status = False
        elif check2 == "checked":
            settings.contact_status = True

        if name is not None:
            settings.site_name = name

        settings.save()

    context = {}
    has_notif(context, request)
    return render(request, 'cinema/Admin.html', context=context)
   

@login_required(login_url = "login")
def contactPage(request):
    if request.method == 'POST':
        text = request.POST.get('message')
        message = Message(sender=request.user, text=text)                  
        message.save()
       
    messages = Message.objects.filter(sender = request.user)
    context = {'messages' : messages}
    has_notif(context, request)
    settings = context['settings']
    if settings.contact_status == True:
        return render(request, 'cinema/Contact.html', context=context)
    else:
        return render(request, "cinema/ContactDisabled.html", context=context)    

@login_required(login_url = "login")
def deleteMessagePage(request, msg_nr):
    instance = Message.objects.get(id=msg_nr)
    instance.delete()
    return redirect('contact')


def schedulePage(request):
    today = pendulum.now()
    start = today.start_of('week').to_date_string()
    end = today.end_of('week').to_date_string()
    shows = Show.objects.filter(date__range = [start, end], date__gte=date.today())
    
    movies = []
    for show in shows:
        if show.movie_ID not in movies:
            movies.append(show.movie_ID)
    
    shows_list = []
    for movie in movies:
        movie_shows = Show.objects.filter(movie_ID = movie, date__range = [start, end], date__gte=date.today())
        t = (movie, movie_shows)
        shows_list.append(t)


    context = { 'movies' : movies, 
                'shows_list' : shows_list 
                }
    has_notif(context, request)
    return render(request, 'cinema/Schedule.html', context=context)

@allowed_users(allowed_roles=['admin', 'employee'])
def createMoviePage(request):
    context ={}
    form = MovieForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect("employee")
    context['form']= form
    has_notif(context, request)
    return render(request, "cinema/CreateMovie.html", context=context)

@allowed_users(allowed_roles=['admin', 'employee'])
def createShowPage(request):
    context ={}
    form = ShowForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect("employee")
    context['form']= form
    has_notif(context, request)
    return render(request, "cinema/CreateShow.html", context=context)

@login_required(login_url = "login")
def ticketPage(request, show_nr):
    myShow = Show.objects.filter(id=show_nr)[0]
    av_seats = ShowSeat.objects.filter(show_ID = myShow, booked=False).count()
    all_seats = ShowSeat.objects.filter(show_ID = myShow)
    tickets = Ticket.objects.all()
    context = {'show_nr' : show_nr,
                'my_show' : myShow,
                'av_seats' : av_seats,
                'tickets' : tickets,
                'all_seats' : all_seats}
    if request.method == 'POST':
        seats = request.POST.get('total_seats')
        price = request.POST.get('total_price')
        curr_time = datetime.now()
        if seats != None:
            book = Booking(show_id=myShow, user_id=request.user, nr_of_seats=seats, booking_time=curr_time, total_price=price)
            book.save()
            context['booking'] = book

        return redirect("http://localhost:8080/cinema/selectseats"+str(show_nr)+"_"+str(book.id)) 

    has_notif(context, request)
    settings = context['settings']
    if settings.bookings_status == True:    
        return render(request, "cinema/Ticket.html", context=context)
    else:
        return render(request, "cinema/BookingsDisabled.html", context=context)    

@login_required(login_url = "login")
def selectSeatsPage(request, show_booking):
    tokens = show_booking.split("_")
    show_nr = int(tokens[0])
    booking_id = int(tokens[1])
    myShow = Show.objects.filter(id=show_nr)[0]
    av_seats = ShowSeat.objects.filter(show_ID = myShow, booked=False).count()
    all_seats = ShowSeat.objects.filter(show_ID = myShow)
    tickets = Ticket.objects.all()
    occupied_seats = ShowSeat.objects.filter(show_ID = myShow, booked=True)
    occ_seats_nr = []
    for seat in occupied_seats:
        occ_seats_nr.append(seat.seat_nr)

    booking = Booking.objects.filter(id=booking_id)[0]
    context = {'show_nr' : show_nr,
        'my_show' : myShow,
        'av_seats' : av_seats,
        'tickets' : tickets,
        'all_seats' : all_seats,
        'booking' : booking}
    context['occ_seats_nr'] = occ_seats_nr   
    
    if request.method == 'POST':
        selected_seats = request.POST.get('selected_seats')
        list_of_strings = selected_seats.split(' ')[1:]
        list_of_integers = list(map(int, list_of_strings))
        for nr in list_of_integers:
            showseat = ShowSeat.objects.filter(show_ID=myShow, seat_nr=nr)[0]
            showseat.booked = True
            showseat.save(update_fields=['booked'])
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size = 15)
        pdf.cell(200, 10, txt = "Bilet CinemaCity",
                ln = 1, align = 'C')
        
        pdf.cell(200, 10, txt = "Spectacol: " + str(myShow),
                ln = 2, align = 'L')

        pdf.cell(200, 10, txt = "Locurile cumparate: " + selected_seats,
                ln = 3, align = 'L')
        
        pdf.cell(200, 10, txt = "Pret: " + str(booking.total_price) + " lei",
                ln = 4, align = 'L')

        pdf.output("../Bilet_" + str(request.user) + "_" + str(booking.id) + ".pdf")
        
        return redirect("success")

    has_notif(context, request)          
    return render(request, "cinema/SelectSeats.html", context=context)
    
@login_required(login_url = "login")
def successPage(request):
    return render(request, "cinema/SuccessTicket.html")

def notificationPage(request):
    my_notifications = Notification.objects.filter(user_id=request.user)
    context = {'my_notifications' : my_notifications}
    has_notif(context, request)
    return render(request, "cinema/Notification.html", context=context)

def deleteNotificationPage(request, notif_nr):
    instance = Notification.objects.get(id=notif_nr)
    instance.delete()
    return redirect('notification')

@allowed_users(allowed_roles=['admin'])
def viewClients(request):
    context = {'clients': User.objects.all()}
    has_notif(context, request)
    return render(request, "cinema/Clients.html", context=context)   

@allowed_users(allowed_roles=['admin'])
def addEmployee(request):
    context ={}
    form = EmployeeForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
    context['form']= form

    all_employees = Employee.objects.all()
    context['employees'] = all_employees
    has_notif(context, request)
    return render(request, "cinema/AddEmployee.html", context=context)                  

@allowed_users(allowed_roles=['admin'])
def modifyPrice(request):
    tickets = Ticket.objects.all()

    if request.method == "POST":
        price_student = request.POST.get('modify-price-Student')
        price_adult = request.POST.get('modify-price-Adult')
        price_elev = request.POST.get('modify-price-Elev')
        price_pensionar = request.POST.get('modify-price-Pensionar')
        price_copil = request.POST.get('modify-price-Copil')

        if price_student != None:
                record = Ticket.objects.filter(category='Student')[0]
                record.price = price_student
                record.save(update_fields=['price'])

        if price_adult != None:
                record = Ticket.objects.filter(category='Adult')[0]
                record.price = price_adult
                record.save(update_fields=['price'])

        if price_elev != None:
                record = Ticket.objects.filter(category='Elev')[0]
                record.price = price_elev
                record.save(update_fields=['price'])

        if price_pensionar != None:
                record = Ticket.objects.filter(category='Pensionar')[0]
                record.price = price_pensionar
                record.save(update_fields=['price'])
        
        if price_copil != None:
                record = Ticket.objects.filter(category='Copil')[0]
                record.price = price_copil
                record.save(update_fields=['price'])

    context = {"tickets":tickets}
    has_notif(context, request)
    return render(request, "cinema/ModifyTicketPrice.html", context=context)   


@allowed_users(allowed_roles=['admin'])
def viewStatistics(request):
    now = timezone.now()
    year = now.year
    context = {}

    for month in range(1,13):
        num_days = calendar.monthrange(year, month)[1]
        dates = [date(year, month, day) for day in range(1, num_days+1)]
        shows = Show.objects.filter(date__range=(dates[0], dates[-1]))
        total_sum = 0
        views_dict = {}
        for show in shows:
            bookings = Booking.objects.filter(show_id = show)
            bought_tickets = ShowSeat.objects.filter(show_ID=show, booked=True).count()
            movie = show.movie_ID
            if movie not in views_dict:
                views_dict[movie] = bought_tickets
            else:
                views_dict[movie] = views_dict[movie] + bought_tickets    

            for booking in bookings:
                total_sum = booking.total_price + total_sum

        max_views = 0
        max_movie = ""
        for key in views_dict:
            if views_dict[key] > max_views:
                max_views = views_dict[key]
                max_movie = key

        context['v'+str(month)] = max_movie     
        context['l'+str(month)] = total_sum

    has_notif(context, request)   
    return render(request, "cinema/ViewStatistics.html", context=context)

@allowed_users(allowed_roles=['admin'])
def deleteEmployeePage(request, employee_id):
    my_empl = Employee.objects.get(id=employee_id)
    my_empl.delete()
    return redirect('add-employee')
