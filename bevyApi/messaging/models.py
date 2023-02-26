from django.db import models

# the Room model holds the unique pair of two users in a chat room
class Room(models.Model):
    user1 = models.CharField(max_length=100)
    user2 = models.CharField(max_length=100)

    def __str__(self):
        return "user1: " + self.user1 + " user2: " + self.user2


# Messages related to a Room (chat) will be deleted when the Room is deleted
class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, db_index=True)
    sender = models.CharField(max_length=100, null=False, blank=False)
    recipient = models.CharField(max_length=100, null=False, blank=False)
    title = models.CharField(max_length=100, null=False, blank=False)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    # class Meta:
    #     ordering = ['created_at']

    def __str__(self):
        return self.sender + " to " + self.recipient + ": " + self.title
