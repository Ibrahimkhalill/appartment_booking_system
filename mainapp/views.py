from django.shortcuts import render, redirect
from mainapp.models import *
# Create your views here.
import datetime
from django.contrib import messages
from django.http import JsonResponse 
from django.utils.encoding import force_bytes, force_str 
# from .tokens import account_activation_token  
   
from django.contrib.sites.shortcuts import get_current_site  
from django.template.loader import render_to_string 
from django.utils.http import urlsafe_base64_encode ,urlsafe_base64_decode   
from django.core.mail import EmailMessage   
from django.contrib.auth import login as Login_process ,logout,authenticate, get_user_model

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from mainapp.models import *
from mainapp.serializers import ContactSerializer
from rest_framework import generics
from rest_framework import mixins
from rest_framework.authentication import SessionAuthentication, BasicAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView


class ContactList(generics.ListCreateAPIView,mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes =[TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
class ContactDetail(generics.RetrieveUpdateDestroyAPIView,mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


def home(request):
    return render(request, "mainapp/index.html")


def contact(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        phone_number = request.POST['phone_number']
        message = request.POST['messages']
        data = Contact(name=name, email=email,
                       phone_number=phone_number, message=message)
        data.save()
        messages.success(request, "Your Message Send Successfully")
        return redirect('/contact/')
    else:
        return render(request, "mainapp/contact.html")


def room(request):
    data = Room.objects.all()

    context = {
        "rooms": data
    }
    return render(request, "mainapp/our_room.html", context)


def reservation(request, room_id):
    room = Room.objects.filter(pk=room_id)
    if room.count() == 1:
        room = room[0]
        if request.method == "POST":
            name = request.POST.get('name')
            phone_number = request.POST.get('phone_number')
            email = request.POST.get('email')
            check_in = request.POST.get('check_in')
            check_out = request.POST.get('check_out')
            amount = request.POST.get('amount')

            start_date = datetime.datetime.strptime(
                check_in, "%Y-%m-%d").date()
            end_date = datetime.datetime.strptime(check_out, "%Y-%m-%d").date()
            no_of_days = (end_date-start_date).days
            bill = room.price*int(no_of_days)
            print(bill)
            data = Reservation(room_no=room, name=name, phone_number=phone_number, email=email,
                               check_in_date=check_in, check_out_date=check_out, amount=bill)
            data.save()

            current_site_info = get_current_site(request)  
            mail_subject = 'New Room Booking alert'  
            message = render_to_string('mainapp/acc_active_email.html', {  
                'user': name,  
                'phone_number': phone_number,  
                'email': email,  
                'check_in':check_in,  
                'check_out': check_out,
                'room': room,
            })  
            to_email = 'mdibrahimkhalil516@gmail.com'
            email = EmailMessage(  
                        mail_subject, message, to=[to_email]  
            )  
            email.send()  
               
        
            context = {

                "start_date": check_in,
                "end_date": check_out,
                "bill": bill,
                "data": room,
                "no_of_days": no_of_days

            }
            return render(request, "mainapp/reservation_confirm.html", context)

        else:
            context = {
                "room_id": room_id,
                "room": room
            }
            return render(request, "mainapp/reservation.html", context)


def get_date(request):
    if request.method == "POST":

        room_id = request.POST['room_no']
        room = Room.objects.filter(room_no = room_id)[0]
        check_in = request.POST['check_in']
        check_out = request.POST['check_out']
        # price = request.POST['price']
        # start_date = datetime.datetime.strptime(check_in, "%Y-%m-%d").date()
        # end_date = datetime.datetime.strptime(check_out, "%Y-%m-%d").date()
        # no_of_days = (end_date-start_date).days
        # print(no_of_days)
        # bill = price*int(no_of_days)

        # print(bill)
        date = Reservation.objects.filter(
            room_no=room, check_in_date=check_in, check_out_date=check_out)
        date = date.count()
        print(date)
        # list= []
        # list.append(
        #     bill,
        #     date
        # )
        return JsonResponse(date, safe=False)


def available_room(request):
    if request.method == "POST":
        check_in = request.POST['check_in']
        check_out = request.POST['check_out']
        check = Reservation.objects.get(
            check_in_date=check_in, check_out_date=check_out)
        room_no = check.room_no.room_no
        print(room_no)
        rooms = Room.objects.all()
        list = []
        for room in rooms:
            if room.room_no == room_no:
                pass
            else:
                list.append(room)
        context = {
            "list": list
        }
        return render(request, "mainapp/available_room.html", context)
    else:

        return render(request, "mainapp/available_room.html")
