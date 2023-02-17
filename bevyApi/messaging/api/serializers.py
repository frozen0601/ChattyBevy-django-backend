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
            'sender',
            'recipient',
            'title',
            'body',
        ]

    def validate(self, data):
        sender = data.get('sender')
        recipient = data.get('recipient')
        title = data.get('title')
        body = data.get('body')

        if sender is None:
            raise serializers.ValidationError("Sender field is required.")
        if recipient is None:
            raise serializers.ValidationError("Recipient field is required.")
        if title is None:
            raise serializers.ValidationError("Title field is required.")
        if body is None:
            raise serializers.ValidationError("Body field is required.")

        if sender == recipient:
            raise serializers.ValidationError("Sender and Recipient cannot be the same.")

        return data


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'user1', 'user2']

    def validate(self, data):
        user1 = data.get('user1')
        user2 = data.get('user2')

        if user1 is None or user2 is None:
            raise serializers.ValidationError("User1 and User2 fields are required.")

        if user1 == user2:
            raise serializers.ValidationError("User1 and User2 cannot be the same.")

        return data
