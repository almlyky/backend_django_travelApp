from django.shortcuts import render,get_object_or_404
from rest_framework.response import Response
from rest_framework import generics,viewsets,status
from .models import *
from .serializers import *
from rest_framework.decorators import api_view


# Create your views here.
class TravelList(generics.ListCreateAPIView):
    queryset=Travel2.objects.all()
    serializer_class=TravelSerializer

class Travelpk(generics.RetrieveUpdateDestroyAPIView):
    queryser= Travel2.objects.all()
    serializer_class = TravelSerializer

# class CustomerList(generics.ListCreateAPIView):
#     queryset = Customer.objects.all()
#     serializer_class = CustomerSerializer

class CustomerList(generics.ListCreateAPIView):
    queryset = Customer2.objects.all()
    serializer_class = CustomerSerializer

    def create(self, request, *args, **kwargs):
        name=request.data['customer_name']
        passport=request.data['customer_passport_number']

        # استخرج البيانات من الطلب
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # تحقق من وجود سجل مطابق
        # customer, created = Customer.objects.get_or_create(
        #     **serializer.validated_data
        # )
        customer=Customer.objects.filter(customer_name=name,customer_passport_number=passport).first()

        # إذا كان السجل موجودًا، قم بإرجاعه مع حالة 200
        if customer:
            return Response(
                self.get_serializer(customer).data,
                status=status.HTTP_200_OK
            )

        # إذا كان السجل جديدًا، قم بحفظه وإرجاعه مع حالة 201
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class Customerpk (generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer2.objects.all()
    serializer_class = CustomerSerializer

class BookingList(generics.ListCreateAPIView):
    queryset = Booking2.objects.all()
    serializer_class = BookingSubSerializer

    def create(self, request, *args, **kwargs):
        # استخراج البيانات من الطلب
        tr_id = request.data['trav_fk']
        coustom_id = request.data['customer_fk']
        # date = request.data['booking_date']
        
        # التأكد من وجود الرحلة والعميل
        tr_data = Travel2.objects.filter(travel_id=tr_id).first()
        coustom_data = Customer2.objects.filter(customer_id=coustom_id).first()
        
        # التحقق من وجود حجز مسبق لنفس العميل على نفس الرحلة
        if Booking2.objects.filter(trav_fk=tr_data, customer_fk=coustom_data).exists():
            return Response({"message": "already_exist"}, status=status.HTTP_200_OK)
        
        # متابعة عملية الحفظ عند عدم وجود تعارض
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(customer_fk=coustom_data, trav_fk=tr_data)
        
        # إرجاع استجابة توضح نجاح الإنشاء
        headers = self.get_success_headers(serializer.data)
        return Response({ 
            "data":serializer.data,
            "message":"success"
            }
            , status=status.HTTP_201_CREATED, headers=headers)



class Bookingpk(generics.RetrieveUpdateDestroyAPIView):
    queryset=Booking2.objects.all()
    serializer_class=BookingSerializer