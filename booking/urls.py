from django.contrib import admin
from django.urls import path 
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('login_view',views.login_view,name='login_view'),
    path('recommend_hall',views.recommend_hall,name='recommend_hall'),
    path('booked_venues',views.booked_venues,name='booked_venues'),
    path('register',views.register,name='register'),
    path('venue_list',views.venue_list,name='venue_list'),
    path('book_venue',views.book_venue,name="book_venue"),
    path('details',views.details,name='details'),
    path('approval',views.approval,name="approval"),
    path('history',views.history,name="history"),
    path('dashboard',views.dashboard,name="dashboard"),
    path('admin',views.admin,name="admin"),
    path('upcoming', views.upcoming, name="upcoming")
]