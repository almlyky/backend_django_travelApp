from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView


urlpatterns=[
    # path('login/',views.login),
     path('register_google/', views.GoogleLoginAPIView.as_view()),
    path("signup/",views.signUp),
    path("userinfo/",views.getuseer),
    path('update/',views.updateuser),
    path("gettoken/",TokenObtainPairView.as_view()),
    path('forgetpassword/',views.forgerpassword),
    path('resetepassword/<str:token>/',views.resetpassword),
    path('checkotp/',views.verify_otp)
]