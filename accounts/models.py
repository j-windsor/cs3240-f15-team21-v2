from django.db import models

# Create your models here.

from django.contrib.auth.models import User

class Security(models.Model):
    user = models.OneToOneField(User)
    pem_key = models.CharField(max_length=1000, default="key")
    public_key = models.CharField(max_length=1000, default="key")

def get_unread(self):
    return self.recipient.filter(unread=True).count()

User.add_to_class('get_unread', get_unread)

#public_key = models.CharField(max_length=1000, default="key")
#public_key.contribute_to_class(User, 'public_key')

#pem_key = models.CharField(max_length=1000, default="key")
#pem_key.contribute_to_class(User, 'pem_key')
