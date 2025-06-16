from typing import Literal
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import User
from djoser.serializers import UserCreateSerializer

from django.contrib.auth.models import User
from rest_framework import serializers

class Myserializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        fields=['email','username','password']

        

class SignUpSerializers(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['username','email','password']
        
        extra_kwargs = {
            'username': {'required':True ,'allow_blank':False},
            'email' : {'required':True ,'allow_blank':False},
            'password' : {'required':True ,'allow_blank':False,'min_length':5}
        }

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['pk','email', 'username','is_active']


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        email = attrs.get("username")  # استخدم "username" كمدخل للإيميل
        password = attrs.get("password")

        # البحث عن المستخدم باستخدام الإيميل فقط
        user = User.objects.filter(email=email).first()

        # إذا لم يتم العثور على المستخدم
        if not user:
            raise AuthenticationFailed("No user found with the provided email.")

        # التحقق من كلمة المرور
        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect password.")

        # التحقق من حالة المستخدم إذا كان غير نشط
        if not user.is_active:
            raise AuthenticationFailed("This user account is inactive.")

        # السماح بالوصول إذا كان كل شيء صحيحًا
        attrs['user'] = user
        return super().validate(attrs)
