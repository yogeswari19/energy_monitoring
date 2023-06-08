from django.db import models
import datetime
from djmoney.models.fields import MoneyField


# Create your models here.
class bookvenue(models.Model):
    name=models.CharField(max_length=255,null=False)
    email=models.EmailField()
    venue=models.CharField(max_length=255, default='venue name xyz',null=True)
    staff_coordinator=models.CharField(max_length=255,default='xyz',null=True)
    event_name=models.CharField(max_length=255, default='event name xyz')
    club_name=models.CharField(max_length=255,  default='club')
    event_desp=models.TextField(default='event description')
    booked_date=models.DateTimeField(auto_now_add=True,null=True)
    start_date=models.DateField(default=datetime.date.today)
    end_date=models.DateField()
    start_time=models.TimeField()
    end_time=models.TimeField()
    aud_count=models.IntegerField(default=0)
    status=models.BooleanField(null=True)
    contact_number = models.CharField(max_length=20,null=True)
    requirements = models.CharField(max_length=255,null=True)
    event_budget = MoneyField(max_digits=10, decimal_places=2, default_currency='INR',default=0)

    
