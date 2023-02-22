from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Room(models.Model):
    users = models.ManyToManyField(User)

    def __str__(self):
        return f"{self.id}, {', '.join(str(user) for user in self.users.all())}"


class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    title = models.CharField(max_length=255)
    body = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} to {self.recipient} - {self.title}"
