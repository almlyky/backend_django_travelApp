from django.db import models

# Create your models here.
class Customer1(models.Model):
    custom_id=models.AutoField(primary_key=True)
    custom_name=models.CharField(max_length=100)
    custom_phone=models.IntegerField()
    custom_gender=models.CharField(max_length=10)
    custom_nationality=models.CharField(max_length=15)
    custom_birthday=models.CharField(max_length=15)
    custom_passport_number=models.IntegerField()
    custom_passport_image=models.CharField(max_length=100)


class Travel1(models.Model):
    travel_id=models.AutoField(primary_key=True)
    travel_from=models.CharField(max_length=30)
    travel_to=models.CharField(max_length=30)
    travel_price=models.IntegerField()
    travel_num_seats=models.IntegerField()
    travel_start_time=models.DateTimeField()
    travel_wait_time=models.FloatField()

class Booking1(models.Model):
    booking_id=models.AutoField(primary_key=True)
    custom_fk=models.ForeignKey(Customer1,on_delete=models.CASCADE)
    travel_fk=models.ForeignKey(Travel1,on_delete=models.CASCADE)
    booking_date=models.DateField(auto_now_add=True)