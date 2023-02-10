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


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = [
            'id',
            'user1',
            'user2',
        ]
