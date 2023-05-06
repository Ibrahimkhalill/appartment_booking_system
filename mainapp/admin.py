from django.contrib import admin

# Register your models here.

from mainapp.models import Reservation,Room,Contact

admin.site.register(Room)
admin.site.register(Reservation)
admin.site.register(Contact)