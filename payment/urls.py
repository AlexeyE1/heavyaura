from django.urls import path
from . import  webhooks
from .views import *


app_name = 'payment'

urlpatterns = [
    path('process/', PaymentProcessView.as_view(), name='process'),
    path('completed/', PaymentCompletedView.as_view(), name='completed'),
    path('canceled/', PaymentCanceledView.as_view(), name='canceled'),
    path('webhook/', webhooks.stripe_webhook, name='webhook'),
]
