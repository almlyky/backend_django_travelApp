from rest_framework import serializers
# from django.contrib.auth.models import User
from .models import *

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Customer1
        fields='__all__'

class TravelSerializer(serializers.ModelSerializer):
    class Meta:
        model=Travel1
        fields='__all__'

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model=Booking1
        fields='__all__'

class BookingSubSerializer(serializers.ModelSerializer):
    travel_fk=TravelSerializer(read_only=True)
    customer_fk=CustomerSerializer(read_only=True)
    class Meta:
        model=Booking1
        fields='__all__'