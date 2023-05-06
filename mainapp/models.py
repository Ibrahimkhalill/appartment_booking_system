from django.db import models
from datetime import date
# Create your models here.


class Room(models.Model):
    room_no = models.CharField(max_length=5)
    room_type = models.CharField(max_length=50)
    is_available = models.BooleanField(default=True)
    price = models.FloatField()
    room_image = models.ImageField(
        upload_to="media", height_field=None, width_field=None, max_length=None, default='0.jpeg')

    def __str__(self):
        return "Room No: "+str(self.room_no)


class Reservation(models.Model):
    room_no = models.ForeignKey(Room, on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email=models.CharField(max_length=100)
    check_in_date = models.DateField(auto_now=False, auto_now_add=False)
    check_out_date = models.DateField(auto_now=False, auto_now_add=False)
    amount = models.FloatField()
    booked_on = models.DateTimeField(auto_now=True, auto_now_add=False)
    def __str__(self):
        return "Booking ID: "+str(self.id)

    @property
    def is_past_due(self):
        return date.today() >self.end_day

class Contact(models.Model):
    name=models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email=models.CharField(max_length=100)
    message=models.TextField(max_length=2000)
    def __str__(self):
        return self.name