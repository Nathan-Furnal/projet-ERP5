from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView
from django.conf import settings

from .forms import UserForm
from .models import User

import xml_rpc as xml_rpc


class IndexView(ListView):
    model = User
    template_name = "odoo_connect/index.html"
    context_object_name = "connection"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['userForm'] = UserForm
        return context


def _write_info(login, username):
    with open(settings.BASE_DIR / '.env', 'w') as f:
        f.write(f"{login},{username}")


def connect(request):
    form = UserForm(request.POST)
    # A Model Form won't be valid if a field is already in the DB (very annoying)
    # We need to try with the else clause to see if the connection to Odoo works
    # Lots of copying code here
    if form.is_valid():
        login, password = form.cleaned_data['login'], form.cleaned_data['password']
        try:
            uid = xml_rpc.connect(login, password)
            if uid:
                User.objects.create(
                    login=login,
                    password=password,
                )
                _write_info(login, password)
                messages.success(request, "Identification succeeded!")
            else:
                messages.error(request, "Identification failed.")
        except ConnectionError:
            messages.error(request, "The 0doo server is not started!")
    else:
        login, password = form.data['login'], form.data['password']  # data and not cleaned_data
        try:
            uid = xml_rpc.connect(login, password)
            if uid:
                user = User.objects.get(
                    login=login,
                    password=password,
                )
                if user:
                    messages.success(request, "Identification succeeded!")
                    _write_info(login, password)
            else:
                messages.error(request, "Identification failed.")
        except ConnectionError:
            messages.error(request, "The 0doo server is not started!")
    # redirection vers le site après la requête POST
    # redirection après la gestion correcte pour empêcher de poster deux fois
    return HttpResponseRedirect(reverse('odoo_connect:index'))
