from django.shortcuts import render
from django.views.generic import ListView


# Create your views here.

class IndexView(ListView):
    model = None
    template_name = "odoo_realtor/index.html"
    context_object_name = "realtor"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
