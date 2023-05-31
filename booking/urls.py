from django.contrib import admin
from django.urls import path 
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('login',views.login,name='login'),
    # path('home',views.home,name='home'),
    path('register',views.register,name='register'),
    path('venue_list',views.venue_list,name='venue_list'),
    # path('venue_list/<str:username>/', views.venue_list, name='venue_list'),
    # path('home/venue_list/', views.venue_list, name='venue_list'),
    path('book_venue',views.book_venue,name="book_venue"),
    path('details',views.details,name='details'),
    path('approval',views.approval,name="approval"),
    path('history',views.history,name="history"),
    path('dashboard',views.dashboard,name="dashboard"),
    path('admin',views.admin,name="admin")
]