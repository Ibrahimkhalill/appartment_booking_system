from rest_framework import serializers
from mainapp.models import *

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['name', 'phone_number', 'email', 'message']