from rest_framework import serializers
from messaging.models import Message, Room


class MessageDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = [
            'id',
            'sender',
            'recipient',
            'title',
            'body',
            'created_at',
        ]


class MessageListSerializer(serializers.ModelSerializer):
    message_details = serializers.HyperlinkedIdentityField(
        view_name='messaging:messaging_detail')

    class Meta:
        model = Message
        fields = [
            'id',
            'room_id',
            'title',
            'message_details',
        ]


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

    # def create(self, validated_data: str) -> Message:
    #     return Message.objects.create(**validated_data)

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = [
            'id',
            'user1',
            'user2',
        ]
