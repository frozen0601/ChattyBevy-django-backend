from rest_framework import serializers
from messaging.models import Message, Room

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

    def __str__(self):
        return f'Message from {self.sender} to {self.recipient} ({self.title})'

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'users']

    def validate(self, data):
        users = data.get('users')

        if len(users) != 2:
            raise serializers.ValidationError("Room must have exactly 2 users.")

        if users[0] == users[1]:
            raise serializers.ValidationError("Users cannot be the same.")

        return data

    def __str__(self):
        users = ", ".join([str(user) for user in self.validated_data['users']])
        return self.id, ", ".join([user.username for user in users.all()])
