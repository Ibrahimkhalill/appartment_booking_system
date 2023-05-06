from django.shortcuts import render, redirect
from django.contrib import messages

# Create your views here.
from mainapp.models import Reservation, Room,Contact

def home(request):
    return render(request, "manager/index.html")


def room(request):
    data = Room.objects.all()

    context = {
        "rooms": data
    }
    return render(request, "manager/our_room.html", context)

def reservation_view(request):
    data = Reservation.objects.all()
    context = {
        "data": data
    }
    return render(request, "manager/reservation_view.html", context)

def contact_view(request):
    data = Contact.objects.all()

    context = {
        "data": data
    }
    return render(request, "manager/contact_view.html", context)

def add_room(request):
    if request.method == "POST" and request.FILES['image']:
        room_no = request.POST['room_no']
        room_type = request.POST['room_type']
        price = request.POST['price']
        room_image = request.FILES['image']
        print(room_image)
        checkroom = Room.objects.filter(room_no=room_no)

        if checkroom.exists():
            messages.error(request, "This Room Already Exists!")
        else:

            room = Room(room_no=room_no, room_type=room_type,
                        price=price, room_image=room_image)
            room.save()
            messages.success(request, "Room Added Successfully")
            return redirect('/manager/add_room/')

    return render(request, "manager/add_room.html")
