from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Message(models.Model):
    sender = models.ForeignKey(User, related_name="sender")
    recipient = models.ForeignKey(User, related_name="recipient")
    unread = models.BooleanField(default=True)
    encrypted = models.BooleanField(default=False)
    subject = models.CharField(max_length=30)
    content = models.CharField(max_length=500)
    key = models.CharField(max_length=80)
    send_date = models.DateField()
