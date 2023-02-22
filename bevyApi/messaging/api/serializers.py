from rest_framework import serializers
from messaging.models import Message, Room

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = [
            'id',
            'room_id',
            'sender',
            'recipient',
            'title',
            'body',
            'created_at',
        ]

        def validate(self, data):
            sender = data.get('sender')
            recipient = data.get('recipient')
            title = data.get('title')
            body = data.get('body')

            if not sender:
                raise serializers.ValidationError("Sender is required.")

            if not recipient:
                raise serializers.ValidationError("Recipient is required.")

            if not title:
                raise serializers.ValidationError("Title is required.")

            if not body:
                raise serializers.ValidationError("Body is required.")

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = [
            'id',
            'user1',
            'user2',
        ]
