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

    def validate_sender(self, sender: str) -> str:
        if len(sender) == 0:
            raise serializers.ValidationError(
                "Please make sure a valid sender is provided",
            )
        return sender

    def validate_recipient(self, recipient: str) -> str:
        if len(recipient) == 0:
            raise serializers.ValidationError(
                "Please make sure a valid recipient is provided",
            )
        return recipient

    def validate_title(self, title: str) -> str:
        if len(title) == 0:
            raise serializers.ValidationError(
                "Please make sure a valid title is provided",
            )
        return title

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
