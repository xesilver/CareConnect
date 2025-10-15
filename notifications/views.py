from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db import transaction
from .models import SMSMessage


@method_decorator(csrf_exempt, name='dispatch')
class TwilioWebhookView(APIView):
    permission_classes = [AllowAny]

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        message_sid = request.data.get('MessageSid', '')
        message_status = request.data.get('MessageStatus', '')
        error_code = request.data.get('ErrorCode', '') or ''
        error_message = request.data.get('ErrorMessage', '') or ''

        if message_sid:
            try:
                sms = SMSMessage.objects.select_for_update().get(message_sid=message_sid)
                mapped_status = {
                    'queued': 'queued',
                    'sent': 'sent',
                    'delivered': 'delivered',
                    'failed': 'failed',
                    'undelivered': 'failed',
                }.get(message_status, sms.status)
                sms.status = mapped_status
                sms.error_code = str(error_code)
                sms.error_message = error_message
                sms.save(update_fields=['status', 'error_code', 'error_message', 'updated_at'])
            except SMSMessage.DoesNotExist:
                pass

        return Response({'ok': True})
