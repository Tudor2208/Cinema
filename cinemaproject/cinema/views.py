from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from .forms import ClientsForm, CreateUserForm, EmployeeForm, MovieForm, PriceForm, ShowForm, BookingForm
from .decorators import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import displayusername
from django.contrib.auth.models import User
from .models import Message, Show, ShowSeat, Ticket, Booking, Employee
import pendulum
from datetime import date, datetime
import calendar
from django.urls import reverse
from fpdf import FPDF

import calendar
import datetime

from django.utils import timezone
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
               'date_joined':request.user.date_joined,
               'password': request.user.password}

    salary = -1

    empl = Employee.objects.filter(user_id=request.user)

    if len(empl) > 0:

        salary = empl[0].salary

    context = {'user': request.user,

               'email': request.user.email,

               'last_name': request.user.last_name,

               'first_name': request.user.first_name,

               'last_login': request.user.last_login,

               'date_joined': request.user.date_joined,

               'password': request.user.password,

               'salary': salary}
               

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
    if request.method == "POST":
        resp = request.POST.get('response')
        id = request.POST.get('aux_field')
        msg = Message.objects.get(id = id)
        msg.response = resp
        msg.save(update_fields=['response'])

    all_messages = Message.objects.all()
    context = {'messages_list' : all_messages}
    return render(request, 'cinema/Employee.html', context=context)

@allowed_users(allowed_roles=['admin'])
def adminPage(request):
    return render(request, 'cinema/Admin.html')
   

@login_required(login_url = "login")
def contactPage(request):
    if request.method == 'POST':
        text = request.POST.get('message')
        message = Message(sender=request.user, text=text)                  
        message.save()
       
    messages = Message.objects.filter(sender = request.user)
    dict = {'messages' : messages}
    return render(request, 'cinema/Contact.html', context=dict)

@allowed_users(allowed_roles=['admin'])
def deleteMessagePage(request, msg_nr):
    instance = Message.objects.get(id=msg_nr)
    instance.delete()
    return redirect('contact')

def schedulePage(request):
    today = pendulum.now()
    start = today.start_of('week').to_date_string()
    end = today.end_of('week').to_date_string()
    shows = Show.objects.filter(date__range = [start, end])
    movies = []
    for show in shows:
        if show.movie_ID not in movies:
            movies.append(show.movie_ID)
    
    shows_list = []
    for movie in movies:
        movie_shows = Show.objects.filter(movie_ID = movie, date__range = [start, end])
        t = (movie, movie_shows)
        shows_list.append(t)


    context = { 'movies' : movies, 
                'shows_list' : shows_list 
                }
    
    return render(request, 'cinema/Schedule.html', context=context)

@allowed_users(allowed_roles=['admin', 'employee'])
def createMoviePage(request):
    context ={}
    form = MovieForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect("employee")
    context['form']= form
    return render(request, "cinema/CreateMovie.html", context=context)

@allowed_users(allowed_roles=['admin', 'employee'])
def createShowPage(request):
    context ={}
    form = ShowForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect("employee")
    context['form']= form
    return render(request, "cinema/CreateShow.html", context=context)

@allowed_users(allowed_roles=['admin'])
def addEmployee(request):
    context ={}
    form = EmployeeForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect("admin")
    context['form']= form
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
        print(price_copil)
        print(price_adult)
        print(price_elev)
        print(price_pensionar)
        print(price_student)


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





    # context ={
    #           'price': request.price,
    #           'category': request.category
    #  }

    # form = PriceForm(request.POST or None, request.FILES or None)
    # if form.is_valid():
    #     form.save()
    #     return redirect("admin")


    return render(request, "cinema/ModifyTicketsPrice.html", {"tickets":tickets})




# @allowed_users(allowed_roles=['admin'])
# def viewClients(request):
#     clients = User.objects.all()
#     client_array = []
#     context ={ 'all_clients' : clients
#     }
#     form = ClientsForm(request.POST or None, request.FILES or None)
#     if form.is_valid():
#         form.save()
#         return redirect("admin")
#     context['clients']= client_array
#     return render(request, "cinema/ViewClients.html", context=context)

# @allowed_users(allowed_roles=['admin'])
# def showusername(request):
#     displaynames = User.objects.all()
#     return render(request, 'cinema/ViewClients.html', {"displayusername": displaynames})

@allowed_users(allowed_roles=['admin'])
def viewClients(request):
    return render(request, "cinema/ViewClients.html", {'clients': User.objects.all()})


@allowed_users(allowed_roles=['admin'])
def viewStatistics(request):

     now = timezone.now()
     year = now.year

     monthly_totals = []

     for month in range(1,13):
         num_days = calendar.monthrange(year, month)[1]
         dates = [datetime.date(year, month, day) for day in range(1, num_days+1)]
         shows = Show.objects.filter(date__range=(dates[0], dates[-1]))
         for show in shows:
            Booking.objects.filter(show_id = show)
            bookings = Booking.objects.filter(show_id = show)
            total = 0
            for booking in bookings:
                #tickets = booking.tickets.all()
                #for ticket in tickets:
                 total = booking.total_price + total
         
     monthly_totals.append({
        
        'total' : total,

    })
     context = {'monthly_totals': monthly_totals}
     return render(request, "cinema/ViewStatistics.html", context=context)

    
    # beg_date = datetime.date(year, month)
    # end_date = datetime(2022,12,31)

    # today = pendulum.now()
    # start = today.start_of('month').to_date_string()
    # end = today.end_of('month').to_date_string()

    # shows = Show.objects.filter(date__range = [beg_date, end_date])

    # for show in shows:
    #     Booking.objects.filter(show_id = show)
    #     bookings = Booking.objects.filter(show_id = show)
    #     total = 0
    #     for booking in bookings:
    #         total = booking.total_price + total

    # context = {
    #             'total_price' : total
    # }








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

        return redirect("http://localhost:8080/cinema/selectseats"+str(show_nr)) 
        
    return render(request, "cinema/Ticket.html", context=context)

@login_required(login_url = "login")
def selectSeatsPage(request, show_nr):
    myShow = Show.objects.filter(id=show_nr)[0]
    av_seats = ShowSeat.objects.filter(show_ID = myShow, booked=False).count()
    all_seats = ShowSeat.objects.filter(show_ID = myShow)
    tickets = Ticket.objects.all()
    occupied_seats = ShowSeat.objects.filter(show_ID = myShow, booked=True)
    occ_seats_nr = []
    for seat in occupied_seats:
        occ_seats_nr.append(seat.seat_nr)

    booking = Booking.objects.filter(show_id=myShow, user_id=request.user)[0]
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

        pdf.output("../Bilet_" + str(request.user) + ".pdf")
        
        return redirect("success")      
    return render(request, "cinema/SelectSeats.html", context=context)
    
@login_required(login_url = "login")
def successPage(request):
    return render(request, "cinema/SuccessTicket.html")        


