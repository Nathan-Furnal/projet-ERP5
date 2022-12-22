from .views import HomeView
from django.urls import path
application_name = "home"

urlpatterns = [
    path('', HomeView.as_view(), name="home")
]