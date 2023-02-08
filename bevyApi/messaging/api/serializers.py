import datetime
from rest_framework import serializers
from messaging.models import Message

last_received_time = None


class MessageSerializer(serializers.ModelSerializer):
    last_recieved_time = serializers.SerializerMethodField('_get_last_received_time')
    # last_recieved = serializers.SerializerMethodField('_get_last_received')

    def _get_last_received_time(self, message_object):
        global last_received_time
        if last_received_time is None or last_received_time < message_object.created_at:
            last_received_time = message_object.created_at
        return last_received_time

    class Meta:
        model = Message
        fields = [
            'sender',
            'recipient',
            'title',
            'body',
            'created_at',
            'last_recieved_time'
        ]
        # fields = [
        #     'sender',
        #     'recipient',
        #     'title',
        #     'body',
        #     'created_at',
        # ]
