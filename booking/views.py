from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib.auth import login
import sweetify
from django.contrib import messages
from .models import bookvenue
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth import authenticate
import json
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    return render(request, 'login.html')


# @login_required
def login_view(request):
    if request.method == 'POST':
        user_type = request.POST.get('user-type')
        email = request.POST.get('email')
        print("email",email)
        password = request.POST.get('password')
        print("password",password)
        if user_type == 'user':
            print("user")
            authenticated_user = authenticate(request, email=email, password=password)
            print(authenticated_user)
            if authenticated_user is not None:
                print("not none")
                login(request, authenticated_user)
                return render(request, 'venues.html')
            else:
                print("invalid")
                return render(request, 'login.html', {'invalid_credentials': True})
                
        elif user_type == 'admin':
            print("admin")
            events = bookvenue.objects.all()
            print(events)
            return render(request,'admin.html',{'events': events})
   
def admin(request):
    events = bookvenue.objects.all()
    print(events)
    return render(request,'admin.html',{'events': events})
   
def register(request):
    print("register view")
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        contact_number=request.POST['contact_number']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        username_taken = False
        email_exists = False
        if password==confirm_password:

            if User.objects.filter(username=name).exists():
                username_taken = True
                print('Username taken')
            elif User.objects.filter(email=email).exists():
                print("email check")
                email_exists = True
                return JsonResponse({'success': False, 'message': 'Email already exists,kindly login to book venues'})
              
            else:
                user = User.objects.create_user(username=name,password=password,email=email)
                user.save()
                return JsonResponse({'success': True})
                # print('user created')
                # return render(request,'login.html')

        return JsonResponse({'email_exists': email_exists, 'username_taken': username_taken})
            
    else:
        return render(request,'newuser.html')


def venue_list(request):
    # username = request.session.get('username')
    # print("username",username) 
    # context = {'username': username}
    # return render(request, 'venues.html', context)
    return render(request, 'venues.html')


def recommend_hall(request):
    if request.method == 'POST':
        user = request.user
        print("recommend_hall",user)
        aud_count=request.POST.get('count')
        if 100<int(aud_count)<250:
            halls=['Swami Vivekananda Hall','CV Raman Hall','C block Seminar Hall']
        
        if int(aud_count)>500:
            halls=['Ramanda Adigalar Auditorium']

        if int(aud_count)<20:
            halls=['Conference Room']
        
        if int(aud_count)<100:
            halls=['Lecture Theatre']
        
        context = {
            'halls': halls,
            'aud_count': aud_count
        }
        return render(request, 'venues.html', context)


def check_venue_availability(start_date, end_date, start_time, end_time, venue):
    bookings = bookvenue.objects.filter(
        venue=venue,
        start_date__lte=end_date,
        end_date__gte=start_date,
        start_time__lte=end_time,
        end_time__gte=start_time
    )
    if bookings.exists():
        return True
    else:
        return False



def book_venue(request):
    if request.method=='GET':
        venue=request.GET.get('hall')
        print('venue',venue)
        request.session['venue'] = venue 
        return render(request, 'availability.html')
        
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        is_available = request.POST.get('is_available')
        venue = request.session.get('venue')
        
        is_available = check_venue_availability(start_date, end_date, start_time, end_time, venue)
        # print(is_available)

        context = {
            'is_available': is_available,
            'start_date':start_date,
            'end_date': end_date,
            'start_time': start_time,
            'end_time': end_time,
            'venue':venue
            
        }
        return render(request, 'availability.html', context)

    return render(request, 'availability.html', context)

@login_required(login_url='login_view')
def details(request):
    if request.user.is_authenticated:
        print("Auth True")
        print("Details")
        if request.method=="POST":
            obj=bookvenue()
            obj.event_name = request.POST.get('event_name')
            obj.club_name = request.POST.get('club_forum')
            obj.event_desp = request.POST.get('event_description')
            obj.staff_coordinator = request.POST.get('staff_coordinator')
            # obj.requirements = request.POST.get('requirements')
            obj.event_budget = request.POST.get('event_budget')
            obj.start_date = request.POST.get('start_date')
            obj.end_date = request.POST.get('end_date')
            obj.start_time = request.POST.get('start_time')
            obj.end_time = request.POST.get('end_time')
            obj.venue = request.session.get('venue')
            obj.user = request.user 
            print("details user",obj.user)
            obj.save()
            print(obj.event_name,obj.club_name,obj.event_desp,obj.staff_coordinator,obj.event_budget,obj.start_date,obj.end_date)
            response_data = {
                    'message': 'Successfully booked. You will be redirected.',
                    'redirect_url': 'venue_list'  # Replace with your desired redirect URL
                }
                
            return HttpResponse(json.dumps(response_data), content_type='application/json')
    else:
        print("Not Logged In")    

@login_required
def booked_venues(request):
    user = request.user
    booked_venues = bookvenue.objects.filter(user=user)
    return render(request, 'bookedlist.html', {'booked_venues': booked_venues})

    
def approval(request):
    print("approval view")
    if request.method=='POST':
        print("approval POST")
        event_id = request.POST.get('event_id')
        status = request.POST.get('status')
        print("status",status)
        if status == 'accept':
            status_value = True
        elif status == 'deny':
            status_value = False
        else:
            status_value = None

        if status_value is not None:
            try:
                event = bookvenue.objects.get(id=event_id)
                event.status = status_value
                event.save()
            except bookvenue.DoesNotExist:
                pass
    
    pending_events = bookvenue.objects.filter(status__isnull=True)
    print("pending_events",pending_events)
    
    return render(request,'approval.html',{'pending_events': pending_events})
    
@login_required
def history(request):
    user = request.user
    booked_venues = bookvenue.objects.filter(user=user)
    print(booked_venues)
    return render(request, 'history.html', {'booked_venues': booked_venues})

def dashboard(request):
    return render(request,'dashboard.html')