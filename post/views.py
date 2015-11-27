import os
from Crypto.Cipher import DES
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto import Random
from django.utils import timezone
from django.shortcuts import render
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from .forms import MessageForm
from django.contrib.auth.models import User
from .models import Message
from django.core.mail import send_mail
# Create your views here.

@login_required
def inbox(request):
    return render(request, 'messages/inbox.html')

@login_required
def delete(request, message_id):
    try:
        Message.objects.get(id=message_id).delete()
        messages.success(request, 'Message Deleted.')
    except:
        messages.warning(request, 'Message Failed to Delete.')
    return HttpResponseRedirect('/messages/inbox')

@login_required
def read(request, message_id):
    message = Message.objects.get(id=message_id)
    if message.recipient.id == request.user.id:
        message.unread = False
        message.save()
        return render(request, 'messages/read.html', {'message': message})
    else:
        return HttpResponseRedirect('/messages/inbox')


@login_required
def new(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        f = MessageForm(request.POST)
        # check whether it's valid:
        if f.is_valid():
            # Save the form data to the database.
            # But dont yet commit, we still have some data to add.
            message = Message()
            message.sender = request.user
            message.subject = f.cleaned_data['subject']
            message.content = f.cleaned_data['content']
            try:
                message.recipient = User.objects.get(username=f.cleaned_data['recipient'])
            except:
                messages.warning(request, 'Message not sent: Recipient username not found!')
                return render(request, 'messages/new.html', {'message_form': f})
            if f.cleaned_data['encrypted']:
                message.encrypted = True
                #thehash = SHA256.new(os.urandom(4))
                #hashstring = thehash.digest()[0:8]
                #message.key = str(hashstring)
                #des = DES.new(hashstring, DES.MODE_ECB)
                #text = str.encode(str(f.cleaned_data['content']))
                #while len(text) % 8 != 0:
                #    text += b'\0'
                message.content = str(des.encrypt(text))
                send_mail('[SecureShare] New Encrypted Message Key',
                 'You have a new message from '+message.sender.username+' with subject \"'+message.subject+'\". The DES key for this message is '+message.key+'.',
                 'secureshare21@yahoo.com', [message.recipient.email], fail_silently=False)
                ####### TODO: ADD ENCRYPTION STUFF
            message.send_date = timezone.now()
            # NOW we can save
            message.save();

            # redirect to a new URL:
            messages.success(request, 'Message Sent')
            return HttpResponseRedirect('/messages/inbox')
        else:
            messages.warning(request, 'Message Failed to Send!')
            return render(request, '/messages/new.html', {'message_form': f})
    # if a GET (or any other method) we'll create a blank form
    else:
        message_form = MessageForm()
        return render(request, 'messages/new.html', {'message_form': message_form})

    return render(request, 'messages/new.html')
