from django.db import models
from django.contrib.auth.models import User 

# Create your models here.
class Companys(models.Model):
    com_api=models.TextField()
    com_name=models.CharField(max_length=50,default="")
    com_image=models.ImageField(upload_to="images/company/%y/%m/%d",default="")
    com_end_travel=models.CharField(max_length=50)
    com_end_add_booking=models.CharField(max_length=50)
    com_end_add_customer=models.CharField(max_length=50,default="/customlist/")
    travel_id=models.CharField(max_length=20,default="id")
    travel_from=models.CharField(max_length=50)
    travel_to=models.CharField(max_length=50)
    travel_price=models.CharField(max_length=50)
    travel_num_seats=models.CharField(max_length=50)
    travel_start_time=models.CharField(max_length=50)
    travel_wait_time=models.CharField(max_length=50)
    customer_id=models.CharField(max_length=20,default="customer_id")
    customer_name=models.CharField(max_length=50,default="customer_name")
    customer_phone=models.CharField(max_length=20,default="customer_phone")
    customer_passport_number= models.CharField(max_length=30,default="customer_passport_id")
    customer_passport_image= models.CharField(max_length=100,default="customer_image")
    customer_gender=models.CharField(max_length=20,default="customer_gender")
    customer_nationality=models.CharField(max_length=20,default="customer_nationality")
    customer_birthday=models.CharField(max_length=20,default="customer_birthday")
    customer_fk=models.CharField(max_length=30,default="customer_fk")
    travel_fk=models.CharField(max_length=30,default="travel_fk")
    booking_date=models.CharField(max_length=30,default="booking_date")
    
    def __str__(self):
        return self.com_name

class Travelers(models.Model):
    id = models.AutoField(primary_key=True)  # يعادل auto increment في SQLite
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=1)  
    name = models.CharField(max_length=255)  # نص غير فارغ
    dob = models.DateField()  # تاريخ الميلاد
    gender = models.CharField(max_length=50, blank=True, null=True)  # يمكن أن يكون فارغًا
    nationality = models.CharField(max_length=100, blank=True, null=True)  # الجنسية
    passport_number = models.BigIntegerField()  # رقم الجواز
    phone_number = models.BigIntegerField()  # رقم الهاتف
    passport_image_path = models.ImageField(upload_to="images/%y/%m/%d") # مسار صورة الجواز

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=1)  
    traveler_fk = models.ForeignKey(Travelers, on_delete=models.CASCADE)  # ربط الحجز بالراكب
    com_name=models.CharField(max_length=100,default="albaraka")
    booking_date = models.DateTimeField(auto_now_add=True)  # تاريخ ووقت الحجز
    departure_date = models.CharField(max_length=100)  # تاريخ ووقت المغادرة
    travel_from = models.CharField(max_length=200)  # مكان المغادرة
    travel_to = models.CharField(max_length=200)  # الوجهة
    status = models.CharField(max_length=50, choices=[('pending', 'قيد الإنتظار'), ('confirmed', 'المؤكدة'), ('cancelled', 'الملغية')], default='pending')  # حالة الحجز
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)  # المبلغ الإجمالي للحجز
    booking_code=models.CharField(max_length=200)
    payment_status = models.CharField(max_length=50, choices=[('cash', 'نقدا'), ('transfer', 'ارسال حوالة')], default='transfer')  # حالة الدفع