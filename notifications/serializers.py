from rest_framework import serializers
from .models import SMSMessage


class SMSMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SMSMessage
        fields = [
            'id', 'to_number', 'body', 'status', 'message_sid',
            'error_code', 'error_message', 'appointment', 'created_at'
        ]

