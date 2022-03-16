from unicodedata import name
from django.urls import path
from . import views

urlpatterns =[
    path('login/', views.loginPage, name="login"),
    path('register/', views.registerPage, name="register"),
    path('logout/', views.logoutUser, name="logout"),
    path('', views.index, name="index"),
    path('destinations', views.destinations, name="destinations"),
    path('place/<int:place_id>', views.place, name="place"),
    path('search', views.searchDestination, name="searchDestination"),
    path('create', views.createRoutes, name="createRoutes"),
    path('get/time', views.getTime, name="getTime"),
    path('travel', views.travel, name="travel"),
    path('seats', views.getRoutes, name="getSeats"),
    path('tickets/<str:route>', views.tickets, name="tickets"),
    path('profile', views.profile, name="profile"),
    path('view_tickets/<str:route>', views.view_tickets, name="view_tickets")
    ]