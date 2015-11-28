from django import forms
from django.contrib.auth.models import User
from .models import Message

class MessageForm(forms.Form):
    recipient = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    subject = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}))
    encrypted = forms.BooleanField(required=False)
    #class Meta:
    #    model = Message
    #    fields = ('recipient', 'subject', 'content', 'encrypted')

class KeyForm(forms.Form):
    pem_file = forms.FileField()
