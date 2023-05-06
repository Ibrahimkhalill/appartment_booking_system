
from django.urls import path
from . import views
urlpatterns = [
   path('dasboard',views.home,name='dasboard'),
   path('reservation_view/',views.reservation_view, name='reservation_view'),
   path('add_room/',views.add_room,name="add_room"),
   path('our_room/',views.room, name='our_room'),
   path('contact_view/',views.contact_view, name = 'contact_view')
]
