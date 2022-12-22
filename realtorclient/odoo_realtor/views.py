from django.contrib import messages
from django.shortcuts import render
from django.conf import settings

import xml_rpc


class ApartView:
    uid = False
    context = {}
    @staticmethod
    def index(request):
        try:
            with open(settings.BASE_DIR / '.env') as f:
                login, password = f.readline().split(',')
            ApartView.uid = xml_rpc.connect(login, password)
            if not ApartView.uid:
                messages.error(request, "No valid credentials, please connect with valid ones!")

            ApartView.context = {'apartments': xml_rpc.get_apartments(ApartView.uid, password)}
        except FileNotFoundError:
            messages.error(request, "Please connect first!")
        except ConnectionError:
            messages.error(request, "Please make sure the Odoo server is running!")

        return render(request, 'odoo_realtor/index.html', ApartView.context)
