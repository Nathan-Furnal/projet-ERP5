from django.urls import path

from .views import IndexView

app_name = 'odoo_connect'

urlpatterns = [
    path('', IndexView.as_view(), name="index"),
]