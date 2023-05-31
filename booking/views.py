from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
import sweetify
from django.contrib import messages
from .models import bookvenue
from django.shortcuts import render
from django.urls import reverse

# Create your views here.

def home(request):
    # if request.method == 'POST':
    #     user_type = request.POST.get('user-type')
    #     print("user_type",user_type)
    #     username = request.POST.get('username')
    #     password = request.POST.get('password')
    #     if user_type == 'user':
    #         request.session['username'] = username  # Store the username in the session
            
    #         return render(request, 'venues.html')
    #         # return render(request,'venues.html')
    #         # return redirect(reverse('venue_list', kwargs={'username': username}))
    #         # return redirect('venue_list', username=username)
    #     elif user_type == 'admin':
    #         print("admin")
    #         events = bookvenue.objects.all()
    #         print(events)
    #         return render(request,'admin.html',{'events': events})
    
    return render(request, 'home.html')

def login(request):
    if request.method == 'POST':
        user_type = request.POST.get('user-type')
        print("user_type",user_type)
        username = request.POST.get('username')
        password = request.POST.get('password')
        if user_type == 'user':
            request.session['username'] = username  # Store the username in the session
            context = {'username': username}
            return render(request, 'venues.html', context)
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
        password = request.POST['password']
        confirm_password = request.POST['password']

        if password==confirm_password:
            if User.objects.filter(username=name).exists():
                print('Username taken')
            elif User.objects.filter(email=email).exists():
                print('email taken')
            else:
                user = User.objects.create_user(username=name,password=password,email=email)
                user.save()
                print('user created')
                sweetify.success(request, 'Successfully registered, login to book venues!')
                return render(request,'home.html')
        
        else:
            print('password not matching...')
        return redirect('/')
    else:
        return render(request,'newuser.html')


def venue_list(request):
    username = request.session.get('username')
    print("username",username) 
    context = {'username': username}
    return render(request, 'venues.html', context)

def book_venue(request):
    if request.method=="POST":
        venue_name = request.POST.get('venue') 
        username = request.POST.get('username')
        print("get venue name",venue_name)
        print("username book venue",username)
        context = {'venue_name': venue_name, 'username':username}
        return render(request, 'book.html', context)
        

def details(request):
   
    if request.method=="POST":
        obj=bookvenue()
        obj.venue=request.POST.get('venue')
        obj.name=request.POST.get('name')
        obj.email=request.POST.get('email')
        obj.event_name=request.POST.get('event_name')
        obj.club_name=request.POST.get('deptname')
        obj.event_desp=request.POST.get('eventdesp')
        obj.booked_date=request.POST.get('bookdate')
        obj.event_date=request.POST.get('eventdate')
        obj.start_time=request.POST.get('startTime')
        obj.end_time = request.POST.get('endTime')
        obj.aud_count=request.POST.get('count')
        
        obj.save()
        
        print("details saved")
        
        return redirect('venue_list')
    
def approval(request):
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
    events = bookvenue.objects.all()
    pending_events = bookvenue.objects.filter(status=None)
    return render(request,'approval.html',{'events': pending_events})
    

def history(request):
    return render(request,'history.html')

def dashboard(request):
    return render(request,'dashboard.html')