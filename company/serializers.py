from rest_framework import serializers
from .models import Companys,Travelers,Booking
 

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model=Companys
        fields="__all__"

class TravelerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Travelers
        fields="__all__"

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'