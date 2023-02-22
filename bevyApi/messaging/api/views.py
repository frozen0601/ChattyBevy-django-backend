from rest_framework.response import Response
from rest_framework import viewsets, serializers, status
from .serializers import MessageSerializer, RoomSerializer
from messaging.models import Message, Room
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
# for sql operations
from django.db.models import Q


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 500

# TODO: implemented destroy() (the ability to delete a room)
class RoomViewset(viewsets.ModelViewSet):
    serializer_class = RoomSerializer
    throttle_scope = "room"
    pagination_class = StandardResultsSetPagination

    # list all rooms
    def get_queryset(self, **kwargs):
        user = self.request.user
        rooms = Room.objects.filter(
            (Q(user1=user) | Q(user2=user))
        )
        return rooms

    # retrieve the rooms that correspond to the current user
    def retrieve(self, request, *args, **kwargs):
        params = kwargs
        # room_id
        roomID = params['pk']

        # check if room actually belongs to the user
        if _has_room_permission(request.user, roomID):
            chatHistory = Message.objects.filter(room_id=roomID)
            serializer = MessageSerializer(chatHistory, many=True)
            return Response(serializer.data)
        else:
            raise serializers.ValidationError(
                "No permission to view this room.")


# check if a user has access to the room with roomID
def _has_room_permission(user, roomID):
    room = Room.objects.filter(Q(user1=user) | Q(user2=user), id=roomID)
    return room.exists()


# @permission_classes([AllowAny]) -> obsolete: default policy (IsAuthenticated) applied globally
class MessageViewset(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    throttle_scope = "messaging"
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        messages = Message.objects.all()
        return messages

    # Create a new message
    def create(self, request, *args, **kwargs):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            message_data = serializer.validated_data
            sender = message_data["sender"]
            recipient = message_data["recipient"]

            # Make sure the message is send by current user.
            if request.user.username != sender:
                raise serializers.ValidationError(
                    "The sender must be the current user.")

            # Get room. If room not exist, create a new one.
            try:
                room = Room.objects.get(
                    (Q(user1=sender) & Q(user2=recipient)) |
                    (Q(user1=recipient) & Q(user2=sender))
                )
            except Room.DoesNotExist:
                room = Room.objects.create(user1=sender, user2=recipient)

            # Create message
            Message.objects.create(room=room,
                                   sender=sender,
                                   recipient=recipient,
                                   title=message_data["title"],
                                   body=message_data.get("body", ""))

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # Invalid input in fields
        raise serializers.ValidationError("Field value invalid. Invalid request.")

    # Delete a message with {message.id}
    def destroy(self, request, *args, **kwargs):
        curUser = request.user
        message = self.get_object()
        if curUser == 'admin' or curUser.username == message.sender:
            message = self.get_object()
            message.delete()
            response_message = {'message': "Item deleted successfully"}
        else:
            raise serializers.ValidationError("No permission to delete.")

        return Response({'message': response_message})
