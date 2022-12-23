from django.urls import path

from . import views
from .views import ApartView

app_name = 'odoo_realtor'

urlpatterns = [
    path('', ApartView.index, name="index"),
    path('create_offer', ApartView.create_offer, name="create_offer")
]