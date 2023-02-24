from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import viewsets, serializers, status
from .serializers import MessageSerializer, RoomSerializer
from messaging.models import Message, Room
from rest_framework.pagination import PageNumberPagination
from django.db import IntegrityError
# for sql operations
from django.db.models import Count



class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 500


class RoomViewset(viewsets.ModelViewSet):
    serializer_class = RoomSerializer
    throttle_scope = "room"
    pagination_class = StandardResultsSetPagination

    def get_queryset(self, **kwargs):
        user = self.request.user
        rooms = Room.objects.filter(users=user)
        return rooms

    def retrieve(self, request, *args, **kwargs):
        room_id = kwargs.get('pk')
        if not _has_room_permission(request.user, room_id):
            raise serializers.ValidationError("No permission to view this room.")
            # return Response({'message': "no permission to view this room"})
        messages = Message.objects.filter(room_id=room_id)
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(messages, request)
        serializer = MessageSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)


class MessageViewset(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    throttle_scope = "messaging"
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        messages = Message.objects.all()
        return messages



    # create a new message
    def create(self, request, *args, **kwargs):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            message_data = serializer.validated_data
            sender = message_data["sender"]
            recipient = message_data["recipient"]
            room_id = kwargs.get('room_id')

            # make sure the message is sent by the current user
            if request.user.id != sender.id:
                raise serializers.ValidationError("The sender must be the current user.")

            room = _get_room(sender, recipient, room_id)

            new_message = Message.objects.create(room=room,
                                                sender_id=sender.id,
                                                recipient_id=recipient.id,
                                                title=message_data["title"],
                                                body=message_data.get("body", ""))
            new_message.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        raise serializers.ValidationError("Field input not valid. Invalid request.")


    # delete a message with {message.id}
    def destroy(self, request, *args, **kwargs):
        curUser = request.user
        message = self.get_object()
        if curUser == 'admin' or curUser.username == message.sender:
            message.delete()
            return Response({'message': "Item deleted successfully"})
        else:
            raise serializers.ValidationError("No permission to delete.")

def _has_room_permission(user, roomID):
    print("user.id: ", user.id)
    rooms = Room.objects.all()
    for room in rooms:
        print(room.id)
    room = Room.objects.filter(users=user.id, id=roomID)
    print("room: ", room)
    return room.exists()

def _get_room(sender, recipient, room_id):
    if room_id == "#":
        # check if a room already exists for the sender and recipient
        room, created = Room.objects.get_or_create(users=sorted([sender, recipient]))
        if not created:
            # If a Room with the same users already exists, retrieve it instead
            room = Room.objects.get(users=sender)
    else:
        # retrieve the existing room with the given room_id
        room = get_object_or_404(Room, id=room_id)
        if not room.users.filter(id=sender.id).exists() or not room.users.filter(id=recipient.id).exists():
            raise serializers.ValidationError("User does not belong to the room.")
    return room
