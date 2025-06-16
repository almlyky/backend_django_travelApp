from typing import NoReturn
from django.shortcuts import render
from .models import Companys,Travelers,Booking
from rest_framework import generics,status
from .serializers import CompanySerializer,TravelerSerializer,BookingSerializer
from django.contrib.auth.models import User
from rest_framework.response import Response


# Create your views here.
class Companylist(generics.ListCreateAPIView):
    queryset=Companys.objects.all()
    serializer_class=CompanySerializer
    
class TravelerList(generics.ListCreateAPIView):
    serializer_class = TravelerSerializer

    def get_queryset(self):
        user_id = self.kwargs.get('userId')
        return Travelers.objects.filter(user=user_id)

    def create(self, request, *args, **kwargs):
        user_id = self.kwargs.get('userId')
        user = User.objects.get(id=user_id)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # التحقق من وجود السجل
        name = serializer.validated_data.get('name')
        customer = Travelers.objects.filter(name=name, user=user).first()

        if customer:
            # السجل موجود بالفعل
            return Response(
                {
                    "data": self.get_serializer(customer).data,
                    "message": "already_exist"
                },
                status=status.HTTP_200_OK
            )
        
        # إنشاء سجل جديد
        serializer.save(user=user)
        return Response(
            {
                "data": serializer.data,
                "message": "success"
            },
            status=status.HTTP_201_CREATED
        )


class TravelerFk(generics.RetrieveUpdateDestroyAPIView):
    queryset=Travelers.objects.all()
    serializer_class=TravelerSerializer

    def destroy(self, request, *args, **kwargs):
        # الحصول على المسافر المحدد
        instance = self.get_object()
        pk = self.kwargs.get('pk')
        booking=Booking.objects.filter(traveler_fk=pk).filter()
        # التحقق مما إذا كان المسافر مرتبطًا برحلات
        if booking:  # Assuming a related name `trips` exists in the relationship
            return Response(
                {
                    "message": "already_exist"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        # إذا لم يكن مرتبطًا برحلات، قم بحذفه
        self.perform_destroy(instance)
        return Response(
            {
                "message": "Traveler deleted successfully."
            },
            status=status.HTTP_200_OK
        )
class BookingList(generics.ListCreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    def get_queryset(self):
        user_id = self.kwargs.get('userId')
        return Booking.objects.filter(user=user_id)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # الحصول على المستخدم من userId في kwargs
        user_id = self.kwargs.get('userId')
        user = User.objects.get(id=user_id)

        # إضافة المستخدم إلى البيانات
        validated_data = serializer.validated_data
        validated_data['user'] = user

        # تحقق من وجود سجل مطابق
        booking, created = Booking.objects.get_or_create(**validated_data)
        if not created:
            return Response(
                {
                    "data": self.get_serializer(booking).data,
                    "message": "already_exist"
                },
                status=status.HTTP_200_OK
            )

        # إذا كان السجل جديدًا، قم بحفظه
        return Response(
            {"data": self.get_serializer(booking).data, "message": "success"},
            status=status.HTTP_201_CREATED
        )

        

# عرض لاسترجاع أو تحديث أو حذف حجز محدد
class BookingFk(generics.RetrieveUpdateDestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    