from django.shortcuts import render
from django.http import HttpResponse
import requests
from requests.auth import HTTPBasicAuth


# Create your views here.

def home(request):
    access_token = getAccessToken(request)
   
    return HttpResponse(f"access_token: {access_token} ")


def getAccessToken(request):
    
    consumer_key = "hkrIGOfMKx1D0wtjaKG3GfDAPq73vLbZ1TVayidMbhn05RuW"
    consumer_secret = "3BEKrkqMjAkBjEAVz4830DvdLjrrfcEOib6JtHtJ1TIGVPGwE8Wn88RIIDgWnDB1"

    endpoint = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

    response = requests.get(endpoint, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    data = response.json()
    access_token = data.get('access_token')
    print(f"access token: {access_token}")
    
    return access_token


# def payment(request):
#     return render('payment.html')