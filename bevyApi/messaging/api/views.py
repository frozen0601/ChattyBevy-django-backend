from rest_framework.response import Response
from rest_framework import viewsets, serializers, status
from .serializers import MessageSerializer, RoomSerializer
from messaging.models import Message, Room
from rest_framework.pagination import PageNumberPagination
# for sql operations
from django.db.models import Q


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
        rooms = Room.objects.filter(
            (Q(user1=user.pk) | Q(user2=user.pk))
        )
        return rooms

    def create(self, request, *args, **kwargs):
        room_data = request.data
        if "user1" not in room_data or "user2" not in room_data:
            raise serializers.ValidationError(
                "Invalid/missing field in POST request.")
        user1 = room_data["user1"]
        user2 = room_data["user2"]
        if user1 == user2:
            raise serializers.ValidationError(
                "User1 and User2 cannot be the same.")
        new_room = Room.objects.create(user1_id=user1, user2_id=user2)
        new_room.save()
        serializer = RoomSerializer(new_room)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        room_id = kwargs.get('pk')
        if not _has_room_permission(request.user, room_id):
            return Response({'message': "no permission to view this room"})
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
            # make sure the message is sent by the current user
            if request.user.id != serializer.validated_data['sender']:
                return Response({'error': 'The sender must be the current user'}, status=status.HTTP_400_BAD_REQUEST)

            message_data = serializer.validated_data
            sender_id = message_data["sender"]
            recipient_id = message_data["recipient"]

            room = Room.objects.filter(
                (Q(user1=sender_id) & Q(user2=recipient_id)) |
                (Q(user1=recipient_id) & Q(user2=sender_id))
            )

            # create a new room if the room does not already exist
            if not room.exists():
                new_room = Room.objects.create(user1_id=sender_id, user2_id=recipient_id)
                new_room.save()

            # get the corresponding room
            room = Room.objects.filter(
                (Q(user1=sender_id) & Q(user2=recipient_id)) |
                (Q(user1=recipient_id) & Q(user2=sender_id))
            ).first()

            new_message = Message.objects.create(room=room,
                                                sender_id=sender_id,
                                                recipient_id=recipient_id,
                                                title=message_data["title"],
                                                body=message_data.get("body", ""))
            new_message.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # No permission to delete
        raise serializers.ValidationError("Invalid request.")

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
    room = Room.objects.filter(Q(user1=user.pk) | Q(user2=user.pk), id=roomID)
    return room.exists()
