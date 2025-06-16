from rest_framework import serializers
from .models import *

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model= Customer2
        fields = "__all__"

class TravelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Travel2
        fields = "__all__"
class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking2
        fields = "__all__"
class BookingSubSerializer(serializers.ModelSerializer):
    travel_fk=TravelSerializer(read_only=True)
    customer_fk=CustomerSerializer(read_only=True)
    class Meta:
        model = Booking2
        fields = "__all__"
