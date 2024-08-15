from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import requests
from requests.auth import HTTPBasicAuth
import base64
from django.utils import timezone
import os
from dotenv import load_dotenv
import json



#Load the dotenv variables from the .env file

load_dotenv()

#.env environment variables.
consumer_key = os.getenv('CONSUMER_KEY')
consumer_secret = os.getenv('CONSUMER_SECRET')
passkey = os.getenv('PASSKEY')

# Create your views here.
    
def home(request):
    access_token = getAccessToken(request)
   
    return HttpResponse(f"access_token: {access_token} ")


def getAccessToken(request):
    
    consumer_key = config('CONSUMER_KEY')
    consumer_secret = config('CONSUMER_SECRET')

    endpoint = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

    response = requests.get(endpoint, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    data = response.json()
    access_token = data.get('access_token')
    print(f"access token: {access_token}")
    
    return access_token

# This function sends a request to the api system, to trigger an stk push on the customer's phone.
def payment(request):    

    if request.method == 'POST':
        phone = request.POST.get('phone')
        amount = request.POST.get('amount')
        
        print(f"Phone: {phone}, Amount: {amount}")

        endpoint = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
        access_token = getAccessToken(request)
        print(f"Access Token: {access_token}")
        headers = { "Authorization": "Bearer %s" % access_token }
        Timestamp = timezone.now()
        times = Timestamp.strftime("%Y%m%d%H%M%S")
        password = "174379" + passkey + times
        password = base64.b64encode(password.encode('utf-8')).decode('utf-8') 

        data = {
            "BusinessShortCode": "174379",
            "Password": password,
            "Timestamp": times,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone,
            "PartyB": "174379",
            "PhoneNumber": phone,
            "CallBackURL": "9ea9-102-0-3-110.ngrok-free.app/callback",
            "AccountReference": "Test Payment",
            "TransactionDesc": "MpesaXpres4U",
           
        }
        print(headers)
        print(data)

        response = requests.post(endpoint, json=data, headers = headers)
        print(response.json())
        return response
     


    return render(request, 'payment.html')

def callback(request):
    
   data = request.json()
   print(data)
   return "ok"