from django.contrib import messages
from django.shortcuts import render
from django.conf import settings

import xml_rpc


def index(request):
    try:
        with open(settings.BASE_DIR / '.env') as f:
            login, password = f.readline().split(',')
            uid = xml_rpc.connect(login, password)
            if not uid:
                messages.error(request, "No valid credentials, please connect with valid ones!")

    except FileNotFoundError:
        messages.error(request, "Please connect first!")
    except ConnectionError:
        messages.error(request, "Please make sure the Odoo server is running!")

    return render(request, 'odoo_realtor/index.html')
