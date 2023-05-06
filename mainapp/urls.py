
from django.urls import path
from . import views
from . import weather_views
urlpatterns = [

   path('',views.home, name='home'),
   path('room/',views.room, name='room'),
   path('reservation/<int:room_id>',views.reservation,name='reservation'),
   path('contact/',views.contact,name='contact'),
   path('get_date',views.get_date,name='get_date'),
   path('available_room/',views.available_room,name="available_room"),


   path('contactapi/', views.ContactList.as_view()),
   path('api_detail/<int:pk>/', views.ContactDetail.as_view()),

   path('index/',weather_views.index,name='index')
]
