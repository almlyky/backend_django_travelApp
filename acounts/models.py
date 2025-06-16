import random
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver 
from django.db.models.signals import post_save
from django.template.loader import render_to_string
from django.core.mail import send_mail



# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User,related_name='profile', on_delete=models.CASCADE)
    reset_password_token = models.CharField(max_length=50,default="",blank=True)
    reset_password_expire = models.DateTimeField(null=True,blank=True)
    vserfi_code=models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

 
@receiver(post_save, sender=User)
def save_profile(sender,instance, created, **kwargs):
    user = instance
    code=str(random.randint(10000, 99999))
    code=f"{code}{user.id}"
    htmlmessage=render_to_string('verfication.html',{'code':code})
    if created:
        profile = Profile(user = user,vserfi_code=code)
        profile.save()
        send_mail(
        "Paswword reset from eMarket",
        f"your link reset password is {code}",
        'abwbkrhmyd479@gmail.com',
        [user.email],
        html_message=htmlmessage
       )