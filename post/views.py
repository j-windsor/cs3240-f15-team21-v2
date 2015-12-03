import os
from Crypto.PublicKey import RSA
from Crypto import Random
from django.utils import timezone
from django.shortcuts import render
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from .forms import MessageForm, KeyForm
from django.contrib.auth.models import User
from .models import Message
from django.core.mail import send_mail
# Create your views here.

@login_required
def inbox(request):
    return render(request, 'messages/inbox.html', {'key_form': KeyForm()})

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
    message.unread = False
    message.save()
    if request.method == 'POST':
        f = KeyForm(request.POST, request.FILES)
        if f.is_valid():
            #try:
            key = RSA.importKey(f.cleaned_data['pem_file'].read(), request.user.security.pem_key)
            content = key.decrypt(message.content)
            return render(request, 'messages/read.html', {'message': message, 'content': content})
            #except:
            #    messages.warning(request, 'Decryption did not occur: PEM file invalid')
            #    return HttpResponseRedirect('/messages/inbox')
        else:
            messages.warning(request, 'Decryption did not occur: File upload error.')
            return render(request, 'messages/inbox.html', {'key_form': f})
    if message.recipient.id == request.user.id:
        return render(request, 'messages/read.html', {'message': message, 'content': message.content.decode('utf-8')})
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
            message.content = f.cleaned_data['content'].encode()
            try:
                message.recipient = User.objects.get(username=f.cleaned_data['recipient'])
            except:
                messages.warning(request, 'Message not sent: Recipient username not found!')
                return render(request, 'messages/new.html', {'message_form': f})
            if f.cleaned_data['encrypted']:
                message.encrypted = True
                key = RSA.importKey(message.recipient.security.public_key, "password")
                message.content = key.publickey().encrypt(message.content, 32)[0]

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
