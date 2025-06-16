from django.urls import path,include
from . import views

urlpatterns = [
    path("company/",views.Companylist.as_view()),
    path("traveler/<int:userId>/",views.TravelerList.as_view()),
    path("traveler/<int:userId>/<int:pk>/",views.TravelerFk.as_view()),
    path("booking/<int:userId>/",views.BookingList.as_view()),
    path("booking/<int:userId>/<int:pk>/",views.BookingFk.as_view()),
]