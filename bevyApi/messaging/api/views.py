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

    # create a new room
    def create(self, request, *args, **kwargs):
        room_data = request.data
        if "user1" not in room_data or "user2" not in room_data:
            raise serializers.ValidationError("Invalid/missing field in POST request.")
        user1 = room_data["user1"]
        user2 = room_data["user2"]
        if user1 == user2:
            raise serializers.ValidationError("User1 and User2 cannot be the same.")
        new_room = Room.objects.create(user1=user1, user2=user2)
        new_room.save()
        serializer = RoomSerializer(new_room)
        return Response(serializer.data)

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
            return Response({'message': "no permission to view this room"})


# check if a user has access to the room with roomID
def _has_room_permission(user, roomID):
        room = Room.objects.filter(Q(user1=user) | Q(user2=user), id=roomID)
        return room.exists()

# in_use: create(), destroy()
# @permission_classes([AllowAny]) -> obsolete: default policy (IsAuthenticated) applied globally
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
            # make sure the message is send by current user
            if request.user.username != serializer.validated_data['sender']:
                return Response({'error': 'The sender must be the current user'}, status=status.HTTP_400_BAD_REQUEST)

            message_data = serializer.validated_data
            sender = message_data["sender"]
            recipient = message_data["recipient"]

            room = Room.objects.filter(
                (Q(user1=sender) & Q(user2=recipient)) |
                (Q(user1=recipient) & Q(user2=sender))
            )

            # create a new room if the room does not already exist
            if not room.exists():
                new_room = Room.objects.create(user1=sender,
                                            user2=recipient)
                new_room.save()

            # get the corresponding room
            room = Room.objects.filter(
                (Q(user1=sender) & Q(user2=recipient)) |
                (Q(user1=recipient) & Q(user2=sender))
            ).first()

            new_message = Message.objects.create(room=room,
                                                sender=sender,
                                                recipient=recipient,
                                                title=message_data["title"],
                                                body=message_data.get("body", ""))
            new_message.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # No permission to delete
        raise serializers.ValidationError("Invalid request.")
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # delete a message with {message.id}
    def destroy(self, request, *args, **kwargs):
        curUser = request.user
        message = self.get_object()
        if curUser == 'admin' or curUser.username == message.sender:
            message = self.get_object()
            message.delete()
            response_message = {'message': "Item deleted successfully"}
        else:
            raise serializers.ValidationError("No permission to delete.")
            # response_message = {'message': "No permission to delete"}

        return Response({'message': response_message})


'''#obsolete/learning area
class MessageListView(ListAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageListSerializer
class MessageDetailView(RetrieveAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageDetailSerializer
    def list(self, request):
        curUser = request.user
        # messages where the curUser takes part of
        usersMessages = Message.objects.filter(
            Q(sender=curUser.username) | Q(recipient=curUser.username))
        serializer = MessageSerializer(usersMessages, many=True)
        return Response(serializer.data)
class MessageViewset(viewsets.ModelViewSet):
    # [DEPRECATED] this the GET result of /messaging/messages/{otherUser}
    # this will show the messages between the user and the otherUser
    # this will be used for the Inbox
    def retrieve(self, request, *args, **kwargs):
        params = kwargs
        otherUser = params['pk']
        curUser = request.user
        chatHistory = Message.objects.filter(
            (Q(sender=curUser.username) & Q(recipient=otherUser)) |
            (Q(sender=otherUser) & Q(recipient=curUser.username))
        )
        serializer = MessageSerializer(chatHistory, many=True)
        return Response(serializer.data)
'''
