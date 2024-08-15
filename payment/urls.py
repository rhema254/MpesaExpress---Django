from django.urls import path
from .views import *

urlpatterns=[
    path('', home, name='home'),
    path('payment/', payment, name='payment'),
    path('callback/', callback, name='callback'),
    
]