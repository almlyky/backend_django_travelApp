from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework import status
from .serializers import SignUpSerializers,UserSerializer
from rest_framework.permissions import IsAuthenticated
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.db.models import Q
from django.conf import settings
from django.template.loader import render_to_string
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer

# Create your views here.

from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

class GoogleLoginAPIView(APIView):
    def post(self, request):
        google_id = request.data.get('google_id')  # استخدم هذا كـ username فريد
        email = request.data.get('email')

        if not google_id or not email:
            return Response({"error": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)

        user, created = User.objects.get_or_create(
            username=google_id,
            defaults={
                'email': email,
            }
        )

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        
        if not created:
            # تحديث بيانات المستخدم إذا كان موجودًا بالفعل
            return Response({
            "message": "User saved successfully",
            "user_id": user.pk,
            "username": user.username,
        }, status=status.HTTP_200_OK)

        return Response({
            "message": "User saved successfully",
            "user_id": user.pk,
            "username": user.username,
            "access_token":access_token
        }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def signUp(requset):
    data=requset.data
    if data['password'] != data['confirmPassword']:
                return Response({'error': 'Password are not same'},status=status.HTTP_400_BAD_REQUEST)
    serializer=SignUpSerializers(data=data)
    if serializer.is_valid():
        if not User.objects.filter(email=data['email']).exists():
            user=User.objects.create(
                username=data['username'],
                email=data['email'],
                password = make_password(data['password']),
                is_active = False
                )
            return Response(
                {'status':'successfuly' },
                    status=status.HTTP_201_CREATED
                    )
        else:
            return Response(
                     {'status':'error', 'message':'This email already exists!' },
                    status=status.HTTP_400_BAD_REQUEST
                )
    else:
        return Response(serializer.errors)  


@api_view(['POST'])
def verify_otp(request):
    try:
        if request.method == 'POST':
            otp = request.data['otp']
            user = User.objects.get(profile__vserfi_code = otp)
            print(user.profile.vserfi_code)
            print(otp)
            # profile = Profile.objects.get(user=user_id)
    
            if str(user.profile.vserfi_code) == str(otp):
                user.is_active = True
                user.profile.vserfi_code = 0
                user.save()
                user.profile.save()
                  # Reset the verification code
                # otp_verification.delete()
                # messages.success(request, 'تم تفعيل الحساب بنجاح!')
                return Response({"status":"success"})
            else:
               return Response({"status":"error"},status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateuser(request):
    user=request.user
    data=request.data
    ser=UserSerializer(user,data=data)
    if ser.is_valid():
        ser.save()
        return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getuseer(requset):
    user=UserSerializer(requset.user)
    if user:
        return Response(user.data)

@api_view(['POST'])
def forgerpassword(request):
    data=request.data
    user=get_object_or_404(User,email=data['email'])
    token=get_random_string(50)
    expire_data=datetime.now()+timedelta(minutes=30)
    user.profile.reset_password_token=token
    user.profile.reset_password_expire=expire_data
    user.profile.save()

    # link=f"http://127.0.0.1:8000/acounts/resetepassword/{token}/"
    link=f"http://192.168.8.40:8000/acounts/resetepassword/{token}/"

    body=f"your link reset password is {link}"
    htmlmessage=render_to_string('email_template.html', {"link":link})

    send_mail(
        "Paswword reset from eMarket",
        body,
        'abubaker773880@gamil.com',
        [data['email']],
        html_message=htmlmessage
    )
    return Response({"details":f"Password reset sent to {data['email']}"})

@api_view(['POST','GET'])
def resetpassword(request,token):
    data=request.data
    user=get_object_or_404(User,profile__reset_password_token = token)
    if request.method=='POST':


        data=request.data
        user=get_object_or_404(User,profile__reset_password_token = token)

        if user.profile.reset_password_expire.replace(tzinfo=None) < datetime.now():
            return Response({'error': 'Token is expired'},status=status.HTTP_400_BAD_REQUEST)
        if data['password']!=data['confirmpassword']:
            return Response({'error': 'Password are not same'},status=status.HTTP_400_BAD_REQUEST)
    
        user.password=make_password(data['password'])
        user.profile.reset_password_token = ""
        user.profile.reset_password_expire = None 
        user.profile.save()
        user.save()
        return Response({'details': 'Password reset done '})
    elif request.method=='GET':
         return render(request,'resetpassword.html')

# @api_view(['GET'])
# def login(request):
#     data=request.data
#     email=data['email']
#     passowrd=make_password(data['password'])

#     user=User.objects.get(Q(email=email) & Q(password=passowrd))
#     if user.username!="":
#         ser=UserSerializer(user,many=False)
#         return Response(ser.data,status=status.HTTP_200_OK)
#     return Response({"message":"emai or password uncorrect"},status=status.HTTP_200_OK)


# @api_view(['POST'])
# def forgot_password(request):
#     data = request.data
#     user = get_object_or_404(User,email=data['email'])
#     token = get_random_string(40)
#     expire_date = datetime.now() + timedelta(minutes=30)
#     user.profile.reset_password_token = token
#     user.profile.reset_password_expire = expire_date
#     user.profile.save()
    
#     # host = get_current_host(request)
#     link = "http://localhost:8000/api/reset_password/{token}".format(token=token)
#     body = "Your password reset link is : {link}".format(link=link)
#     send_mail(
#         "Paswword reset from eMarket",
#         body,
#         "eMarket@gmail.com",
#         [data['email']]
#     )
#     return Response({'details': 'Password reset sent to {email}'.format(email=data['email'])})

 


# @api_view(['POST'])
# def reset_password(request,token):
#     data = request.data
#     user = get_object_or_404(User,profile__reset_password_token = token)

#     if user.profile.reset_password_expire.replace(tzinfo=None) < datetime.now():
#         return Response({'error': 'Token is expired'},status=status.HTTP_400_BAD_REQUEST)
    
#     if data['password'] != data['confirmPassword']:
#         return Response({'error': 'Password are not same'},status=status.HTTP_400_BAD_REQUEST)
    
#     user.password = make_password(data['password'])
#     user.profile.reset_password_token = ""
#     user.profile.reset_password_expire = None 
#     user.profile.save() 
#     user.save()
#     return Response({'details': 'Password reset done '})


