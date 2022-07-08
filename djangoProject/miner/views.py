from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse

import requests

from .models import States, BTCPrices

# Create your views here.

btc_price_url = 'https://api.coindesk.com/v1/bpi/currentprice.json'


def home(request):
    minutes = BTCPrices.objects.all()
    states_info = States.objects.all()

    '''Only have 31 days of data in the model database'''
    if len(minutes) > 44640:
        minutes[0].delete()
    return render(request, 'miner/index.html', {
        "states": states_info,
        "minutes": minutes[0]
    })


@csrf_exempt
def get_price(request):
    if request.method != "POST":
        return HttpResponse("Only POST requests allowed!", status=400)
    price = requests.get(btc_price_url)
    x = price.json()
    if price.status_code == 200:
        p = ""
        for i in x['bpi']['USD']['rate']:
            if i != ',':
                p += i
        btc_price = float(p)
        btc = BTCPrices(price=btc_price)
        btc.save()
        return JsonResponse({'message': "Successfully changed."}, status=200)

