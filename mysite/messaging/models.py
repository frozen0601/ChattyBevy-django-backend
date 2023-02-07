from django.db import models
from django.utils import timezone
from users import models as users

class Message(models.Model):
    sender = models.ForeignKey(users.User)
    recipient = models.ForeignKey(users.User)
    title = models.CharField(max_length=150)
    body = models.CharField(max_length=1000)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.car_model