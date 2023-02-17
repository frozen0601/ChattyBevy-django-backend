from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Room(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rooms1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rooms2')
    # created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user1', 'user2')

    def __str__(self):
        return f"{self.user1} - {self.user2}"


class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    title = models.CharField(max_length=255)
    body = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} to {self.recipient} - {self.title}"
