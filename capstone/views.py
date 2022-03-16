from genericpath import exists
from tkinter import Place
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
import datetime
import json


def loginPage(request):

    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        #Get username and password and lower username before database checks
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        #Check if user exists
        try:
            user = User.objects.get(username = username)
        except:
            messages.error(request, 'User does not exist')
            return render (request, 'capstone/login.html')
        
        #Try to sign in user
        user = authenticate(request, username=username, password=password)

        #Final check
        try:
            login(request, user)
            return redirect('index')
        except:
            messages.error(request, 'Password is not valid')

    return render (request, 'capstone/login.html')



def registerPage(request):

    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        #Get username and passwords
        username = request.POST.get('username').lower()
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        confirmation = request.POST.get('confirmation')

        #Check if username is left blank
        if len(username) < 1:
            messages.error(request, 'Username cant be empty')
            return render(request, 'capstone/register.html')

        #Check if first_name is left blank
        if len(first_name) < 1:
            messages.error(request, 'First Name cant be empty')
            return render(request, 'capstone/register.html')

        #Check if last_name is left blank
        if len(last_name) < 1:
            messages.error(request, 'Last Name cant be empty')
            return render(request, 'capstone/register.html')
        
        #Check if password is left blank
        if len(password) < 1:
            messages.error(request, 'Password cant be empty')
            return render(request, 'capstone/register.html')

        #Check if passwords match
        if password != confirmation:
            messages.error(request, 'Passwords do not match')
            return render(request, 'capstone/register.html')
        
        #Check if user exists
        new = User.objects.filter(username = username)  
        if new.count():  
            messages.error(request, 'User already exist')
            return render(request, 'capstone/register.html')

        #Create user and log him in
        user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name)
        user.save()
        login(request,user)
        messages.success(request, 'User Created Successfully')
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, 'capstone/register.html')
    
def logoutUser(request):
    logout(request)
    return redirect('index')

def index(request):
    # Get all places
    places = Places.objects.all
    context = {"places": places}
    return render(request, "capstone/index.html", context)

def destinations(request):
    #Get all destinations 
    destinations = Places.objects.all
    context = {"destinations": destinations}
    return render (request, "capstone/destinations.html", context)

def place(request, place_id):
    #Get the location the user selected
    place = Places.objects.get(id = place_id)

    #Get all the images of that location
    images = Images.objects.filter(place=place.id)
    context = {
        "place": place,
        "images": images
    }
    return render (request, "capstone/place.html", context)

def searchDestination(request, ):
    if request.method == 'POST':
        #Get the users input
        search = request.POST.get('searchedDestination')

        #Search database for a location matching users input
        destinations = Places.objects.filter(place__contains = search)
        context = {"search": search,'destinations': destinations}
        return render(request, "capstone/destinations.html", context)
    #else return all locations
    else:
        return HttpResponseRedirect(reverse("destinations"))

def createRoutes(request):
    if request.user not in User.objects.filter(is_staff = True):
        return HttpResponseRedirect(reverse("index"))

    if request.method == 'POST':
        # Get Data From Staff User
        dateFrom = datetime.datetime.strptime(request.POST.get('dateFrom'),"%Y, %m, %d").date()
        dateUntil = datetime.datetime.strptime(request.POST.get('dateUntil'),"%Y, %m, %d").date()
        departurePlace = request.POST.get('departurePlace')
        departureTime = request.POST.get('departureTime')
        destinationPlace = request.POST.get('destinationPlace')
        destinationTime = request.POST.get('destinationTime')
        # Get duration from destinationTime - departureTime and convert to hours:mins
        duration = datetime.datetime.strptime(destinationTime,"%H:%M") - datetime.datetime.strptime(departureTime,"%H:%M")
        duration = str(duration)[:-3]

        # Get destination and departure places ID
        departurePlace = Places.objects.get(place = departurePlace)
        destinationPlace = Places.objects.get(place = destinationPlace)

        # Check if places are the same
        if departurePlace == destinationPlace:
            messages.error(request, 'Destination and Departure should be diffrent')
            return HttpResponseRedirect(reverse("createRoutes"))

        # Iterate the dates and save the route
        delta = datetime.timedelta(days=1)
        while dateFrom <= dateUntil:
            try:
                route = Route.objects.create(
                departure = departurePlace,
                destination = destinationPlace,
                departureDay = dateFrom,
                destinationDay = dateFrom,
                departureTime = departureTime,
                destinationTime = destinationTime,
                duration = duration
                )
                route.save()

            except:
                messages.error(request, 'Something went wrong')
                return HttpResponseRedirect(reverse("createRoutes"))
            dateFrom += delta

        messages.success(request, 'Routes Created')
        return HttpResponseRedirect(reverse("createRoutes"))
        
    else:
        context={"places": Places.objects.all}
        return render (request, "capstone/create_routes.html", context)

@login_required
def getTime(request):
    # Put is our fetch method to get the times of departure for the route the user selected
    if request.method == "PUT":

        # Get the data to filter for available routes
        data = json.loads(request.body)
        destination = Places.objects.get(place = data["destination"])
        departure = Places.objects.get(place = data["departure"])
        departureDay = data["departureDay"]

        # Convert places to id
        destination = destination.id
        departure = departure.id

        # Filter through the routes to find the times of departure for the day
        routes = Route.objects.filter(destination = destination, departure = departure, departureDay = departureDay) 

        # Check if there are no routes for that day
        if not routes:
            return JsonResponse({
            "error": "No trips available for that day"
        }, status=400)

        return JsonResponse([route.serialize() for route in routes], safe=False)

def travel(request):
    if request.user.is_authenticated:
        # Get all places
        places = Places.objects.all
        context = {"places": places}
        return render(request, "capstone/travel.html", context)

@login_required
def getRoutes(request):
    # Here we get the route id of the inputs that the user gave us and redirect him to the "set_seats" url so he can choose seats
    if request.method == "POST":
        # Get user's inputs
        departure = Places.objects.get(place = request.POST.get('departurePlace'))
        destination = Places.objects.get(place = request.POST.get('destinationPlace'))
        departureDay = request.POST.get('date')
        departureTime = request.POST.get('departureTime')

        # Check if departure and destination are the same
        if departure == destination:
            messages.error(request, 'departure and destination cannot be identical')
            return HttpResponseRedirect(reverse("travel"))

        # Convert places to id
        destination = destination.id
        departure = departure.id

        # Get the specific route the user is intrested in
        route = Route.objects.get(departure = departure, destination = destination, departureDay = departureDay, departureTime = departureTime)
        seats = Ticket.objects.filter(route = route.id)
        context = {"route": route, "seats": seats}
        return render(request, "capstone/set_seats.html", context)
    else:
        return HttpResponseRedirect(reverse("login"))

@login_required
def tickets(request, route):
    if request.method == "POST":
        seats = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6']
        route = Route.objects.get(id=route)
        counter = 0

        # Iterate through seats and check if there is an input with the name of the seat
        for seat in seats:
            if request.POST.get(seat):
                # Check if tickets are already bought for these seats
                try:
                    Ticket.objects.get(seat = request.POST.get(seat), user = request.user, route = route)
                    messages.error(request, 'These tickets have already be purchased')
                except:
                    # Try to save tickets
                    try:
                        ticket = Ticket.objects.create(seat = request.POST.get(seat), user = request.user, route = route)
                        ticket.save()
                        route.passenger.add(request.user)
                        counter += 1
                    except:
                        messages.error(request, 'Something Went Wrong')
                        return HttpResponseRedirect(reverse("getSeats"))

        # Check if no seats are selected
        if counter == 0:
            messages.error(request, 'You didnt choose any seats')
            return HttpResponseRedirect(request.path_info)
            
        # Get total price and ticket number
        tickets = Ticket.objects.filter(user = request.user, route = route)
        ticketsNum = len(tickets)
        totalPrice = ticketsNum * 15

        messages.success(request, 'Tickets Purchased')
        context = {"tickets": tickets, "route": route, "totalPrice": totalPrice, "ticketsNum": ticketsNum}
        return render(request, "capstone/tickets.html", context)
    else:
        return HttpResponseRedirect(reverse("login"))

def profile(request):
    if request.user.is_authenticated:

        # Get the routes that the user is a passenger
        routes = Route.objects.filter(passenger = request.user)
        print(tickets)
        context = {"routes": routes}
        return render(request, "capstone/profile.html", context)
    else:
        return HttpResponseRedirect(reverse("login"))

def view_tickets(request, route):
    if request.user.is_authenticated:

        # Get the routes that the user is a passenger
        route = Route.objects.get(id=route)

        # Get total price and ticket number
        tickets = Ticket.objects.filter(user = request.user, route = route)
        ticketsNum = len(tickets)
        totalPrice = ticketsNum * 15

        context = {"tickets": tickets, "route": route, "totalPrice": totalPrice, "ticketsNum": ticketsNum}
        return render(request, "capstone/tickets.html", context)
    else:
        return HttpResponseRedirect(reverse("login"))