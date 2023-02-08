from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import viewsets
from .serializers import MessageSerializer
from messaging.models import Message
from django.db.models import Q
from rest_framework.authtoken.models import Token


@api_view()
# @permission_classes([AllowAny])
def firstFunction(request):
    return Response({'message': "we received your request"})

# @permission_classes([AllowAny])


class MessageViewset(viewsets.ModelViewSet):
    serializer_class = MessageSerializer

    def get_queryset(self):
        messages = Message.objects.all()
        return messages

    # the GET result of /messaging/messages/
    # this will be used for the Inbox
    def list(self, request):
        curUser = request.user
        inbox = Message.objects.filter(
            Q(sender=curUser.username) | Q(recipient=curUser.username))
        serializer = MessageSerializer(inbox, many=True)
        return Response(serializer.data)

    # the GET result of /messaging/messages/{otherUser}
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

    def create(self, request, *args, **kwargs):
        message_data = request.data
        new_message = Message.objects.create(sender=message_data["sender"],
                                             recipient=message_data["recipient"],
                                             title=message_data["title"],
                                             body=message_data["body"])
        new_message.save()
        serializer = MessageSerializer(new_message)
        return Response(serializer.data)

    # the DELETE result of /messaging/messages/{message.id}
    # the message can be deleted by the sender or the admin
    def destroy(self, request, *args, **kwargs):
        curUser = request.user
        message = self.get_object()
        if curUser == 'admin' or curUser.username == message.sender:
            message = self.get_object()
            message.delete()
            response_message = {'message': "Item deleted successfully"}
        else:
            response_message = {'message': "No permission to delete"}

        return Response({'message': response_message})
