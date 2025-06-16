from django.db import models

# Create your models here.
class Customer2(models.Model):
    customer_id=models.AutoField(primary_key=True)
    customer_name=models.CharField(max_length=100)
    customer_phone=models.IntegerField()
    customer_gender=models.CharField(max_length=10)
    customer_nationality=models.CharField(max_length=15)
    customer_birthday=models.CharField(max_length=15)
    customer_passport_number=models.IntegerField()
    customer_passport_image=models.CharField(max_length=100)

class Travel2(models.Model):
    CURRENCY_CHOICES = [
        ('USD', 'US Dollar'),
        ('YE', 'Yemeni Riyal'),
        ('SAR', 'Saudi Riyal'),
        # أضف العملات الأخرى هنا
    ]
    travel_id=models.AutoField(primary_key=True)
    trav_from=models.CharField(max_length=30)
    trav_to=models.CharField(max_length=30)
    trav_price=models.IntegerField()
    type_money=models.CharField(max_length=3, choices=CURRENCY_CHOICES,default='YE')
    trav_num_seats=models.IntegerField()
    trav_start_time=models.DateTimeField()
    trav_wait_time=models.FloatField()

class Booking2(models.Model):
    booking_id=models.AutoField(primary_key=True)
    customer_fk=models.ForeignKey(Customer2,on_delete=models.CASCADE)
    trav_fk=models.ForeignKey(Travel2,on_delete=models.CASCADE)
    booking_date=models.DateField(auto_now_add=True)
    