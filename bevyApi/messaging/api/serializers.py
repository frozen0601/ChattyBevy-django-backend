import datetime
from rest_framework import serializers
from messaging.models import Message, Room

# last_received_time = None

# class ContactSerializer(serializers.ModelSerializer):
#     def _get_contact(self, message_object):
#         if (message_object.username != request.user.username):
#             contact = 'userB'
#     return contact

#     class Meta:
#         model = Message
#         fields = [
#             'contact',
#         ]
#         # fields = [
#         #     'sender',
#         #     'recipient',
#         #     'title',
#         #     'body',
#         #     'created_at',
#         # ]

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
    message_details =serializers.HyperlinkedIdentityField(view_name='messaging:messaging_detail')
    class Meta:
        model = Message
        fields = [
            'id',
            'room_id',
            'title',
            'message_details',
        ]

class MessageSerializer(serializers.ModelSerializer):
    # last_recieved_time = serializers.SerializerMethodField('_get_last_received_time')
    # # last_recieved = serializers.SerializerMethodField('_get_last_received')

    # def _get_last_received_time(self, message_object):
    #     global last_received_time
    #     if last_received_time is None or last_received_time < message_object.created_at:
    #         last_received_time = message_object.created_at
    #     return last_received_time


    # rank = serializers.SerializerMethodField('_get_rank')
    # # last_recieved_time = serializers.SerializerMethodField('_get_last_received_time')
    # # # last_recieved = serializers.SerializerMethodField('_get_last_received')

    # def _get_rank(self, message_object):
    #         inbox = message_object.annotate(
    #         # RANK() by price within each store_id
    #         rank=Window(
    #             expression=Rank(),
    #             partition_by=[F('sender'), F('recipient')],
    #             order_by=F('created_at').desc()))
    #     return message_object

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