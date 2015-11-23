from django.db import models

# Create your models here.

from django.contrib.auth.models import User

def get_unread(self):
    return self.recipient.filter(unread=True).count()

User.add_to_class('get_unread', get_unread)

