import xmlrpc.client

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.conf import settings
from .forms import OfferForm
import xml_rpc


class ApartView:
    uid = False
    context = {}
    password = ''

    @staticmethod
    def index(request):
        try:
            with open(settings.BASE_DIR / '.env') as f:
                login, password = f.readline().split(',')
                ApartView.password = password
            ApartView.uid = xml_rpc.connect(login, password)
            if not ApartView.uid:
                ApartView.context = {}
                messages.error(request, "No valid credentials, please connect with valid ones!")

            ApartView.context = {'apartments': xml_rpc.get_apartments(ApartView.uid, password)}
        except FileNotFoundError:
            ApartView.context = {}
            messages.error(request, "Please connect first!")
        except ConnectionError:
            ApartView.context = {}
            messages.error(request, "Please make sure the Odoo server is running!")

        return render(request, 'odoo_realtor/index.html', ApartView.context)

    @staticmethod
    def create_offer(request):
        # See https://docs.djangoproject.com/en/4.1/topics/forms/#the-view
        if request.method == "POST":
            form = OfferForm(request.POST)
            if form.is_valid():
                partner_name = form.cleaned_data['partner_name']
                offer_amt = form.cleaned_data['offer_amt']
                apart_id = form.cleaned_data['apart_id']
                try:
                    xml_rpc.create_offer(ApartView.uid, ApartView.password, partner_name, offer_amt, apart_id)
                except xmlrpc.client.Fault:
                    messages.error(request, "You must input an offer larger than the existing one.")
                return HttpResponseRedirect('/apartments')
        else:
            return render(request, 'odoo_realtor/index.html', ApartView.context)
