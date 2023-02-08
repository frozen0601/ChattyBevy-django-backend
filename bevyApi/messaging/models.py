from django.db import models

class Message(models.Model):
    sender = models.CharField(max_length=100)
    recipient = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    body = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
