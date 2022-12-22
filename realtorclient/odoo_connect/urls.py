from django.urls import path
from . import views
from .views import IndexView

app_name = 'odoo_connect'

urlpatterns = [
    path('', IndexView.as_view(), name="index"),
    path('connect', views.connect, name="connect")
]
