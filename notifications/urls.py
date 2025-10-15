from django.urls import path
from .views import TwilioWebhookView, SMSMessageListView


urlpatterns = [
    path('twilio/webhook/', TwilioWebhookView.as_view(), name='twilio-webhook'),
    path('api/v1/sms/', SMSMessageListView.as_view(), name='sms-list'),
]

