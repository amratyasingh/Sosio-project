from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from rest_framework.response import Response

from django.http import HttpResponseRedirect
from myproject.settings import client_id, client_secret, callback_uri
from django.core.cache import caches
from rest_framework.views import APIView
from re import search
from xero import Xero
from xero.auth import OAuth2Credentials
from xero.constants import XeroScopes

import os

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'


class Home(View):
    def get(self, request, *args, **kwargs):
        return render(request, "index.html")


class XeroOps(APIView):
    def start_xero_auth_view(request):
        credentials = OAuth2Credentials(client_id, client_secret, callback_uri=callback_uri,
                                        scope=[XeroScopes.OFFLINE_ACCESS, XeroScopes.ACCOUNTING_CONTACTS,
                                               XeroScopes.ACCOUNTING_TRANSACTIONS])
        authorization_url = credentials.generate_url()
        caches['default'].set('xero_creds', credentials.state)
        return HttpResponseRedirect(authorization_url)

    def process_callback_view(request):
        cred_state = caches['default'].get('xero_creds')
        if not cred_state:
            print("Error")
            return HttpResponse({"error": "message"})

        credentials = OAuth2Credentials(**cred_state)
        auth_secret = request.get_raw_uri()
        credentials.verify(auth_secret)
        credentials.set_default_tenant()
        caches['default'].set('xero_creds', credentials.state)
        return HttpResponseRedirect("/myapp/")
        # return HttpResponse({"message": "success"})

    def invoice_payload(self, data):
        for key, value in data.items():
            if search("Date", key):
                data[key] = datetime.strptime(value, "%Y-%m-%d")
        return data

    def post(self, request, format=None):
        print(request.data)
        cred_state = caches['default'].get('xero_creds')
        if not cred_state:
            return HttpResponse("<p> Error, you are logged out, please login via /myapp/auth </p>")

        credentials = OAuth2Credentials(**cred_state)
        if credentials.expired():
            credentials.refresh()
            caches['default'].set('xero_creds', credentials.state)

        xero_obj = Xero(credentials)
        payload = self.invoice_payload(request.data)
        print(payload)
        invoice_status = xero_obj.invoices.save_or_put(payload)
        print(invoice_status)
        return Response(invoice_status)
