from rest_framework import serializers
from messaging.models import Message

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
        # fields = [
        #     'sender',
        #     'recipient',
        #     'title',
        #     'body',
        #     'created_at',
        # ]
