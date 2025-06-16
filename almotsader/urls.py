from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    # travel url 
    path('travellist/',views.TravelList.as_view()),
    path('travellist/<int:pk>/',views.Travelpk.as_view()),

    # custom url
    path('customlist/',views.CustomerList.as_view()),
    path('customlist/<int:pk>/',views.Customerpk.as_view()),

    # booking url 
    path('bookinglist/',views.BookingList.as_view()),
    path('bookinglist/<int:pk>/',views.Bookingpk.as_view()),
]