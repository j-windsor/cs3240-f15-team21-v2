from django.db import models

# Create your models here.

from django.contrib.auth.models import User

def get_unread(self):
    return self.recipient.filter(unread=True).count()

User.add_to_class('get_unread', get_unread)

public_key = models.CharField(max_length=1000)
public_key.contribute_to_class(User, 'public_key')

pem_key = models.CharField(max_length=1000)
pem_key.contribute_to_class(User, 'pem_key')
