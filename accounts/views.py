from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from .forms import UserForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.contrib.auth.models import Group, User
from .models import Security
from reports.models import Folder, Report
from Crypto import Random
import random
import string
from Crypto.PublicKey import RSA
from django.core.mail import EmailMessage



# Create your views here.

def register(request):

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            default_folder = Folder()
            default_folder.label = "Uncategorized"
            default_folder.owner = user
            default_folder.save()
            user.folder_set.add(default_folder)
            shared_folder = Folder()
            shared_folder.label = "Shared With Me"
            shared_folder.owner = user
            shared_folder.save()
            user.folder_set.add(shared_folder)

            # Keys for post app
            random_generator = Random.new().read
            key = RSA.generate(1024, random_generator)
            key_security = Security()
            key_security.pem_key = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
            key_security.public_key = key.publickey().exportKey('PEM', "password")
            email = EmailMessage('[SecureShare] Welcome to SecureShare!', 'Welcome to SecureShare '+user.first_name+'! Please save the attached PEM file in a safe place. You will need this to unencrypt any encrypted messages you receive.',
            'secureshare21uva@yahoo.com',
            [user.email])
            email.attach('privatekey.pem', key.exportKey('PEM', key_security.pem_key), 'application/x-pem-file')
            email.send()

            user.save()

            key_security.user = user
            key_security.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print(user_form.errors)

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()

    # Render the template depending on the context.
    return render(request, 'accounts/register.html', {'user_form': user_form, 'registered': registered} )

def user_login(request):

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
                # We use request.POST.get('<variable>') as opposed to request.POST['<variable>'],
                # because the request.POST.get('<variable>') returns None, if the value does not exist,
                # while the request.POST['<variable>'] will raise key error exception
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                # An inactive account was used - no logging in!
                messages.warning(request, 'Your account is disabled. Please contact support.')
                return HttpResponseRedirect('/')
        else:
            # Bad login details were provided. So we can't log the user in.
            # TODO: USE FLASH MESSAGES -----------------
            messages.warning(request, 'Invalid Login.')
            return HttpResponseRedirect(reverse('accounts:login'))

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'accounts/login.html', {})


# Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    messages.success(request, 'You are now logged out.')
    return HttpResponseRedirect('/')

@login_required
def groups(request):
    if request.method == 'POST':
        if request.POST.get('user_name'):
            user_name = request.POST.get('user_name')
            group_name = request.POST.get('group_name')
            try:
                user = User.objects.get(username=user_name)
                group = Group.objects.get(name=group_name)
                user.groups.add(group)
                user.save()
                full_name = user.first_name + " " + user.last_name
                messages.success(request, full_name + " added to group!")
            except:
                messages.warning(request, 'User not added to group: Username not Found!')
        else:
            group_name = request.POST.get('group_name')
            try:
                newgroup = Group()
                newgroup.name = group_name
                newgroup.save()
                request.user.groups.add(newgroup)
                request.user.save()
                messages.success(request, 'Group Created.')
            except:
                messages.warning(request, 'Group Creation Failed. Group Already Exists.')

        return HttpResponseRedirect('/accounts/groups')
    return render(request, 'accounts/groups.html', {})


@user_passes_test(lambda u: u.is_superuser)
def sitemanager(request):
    return render(request, 'accounts/sitemanager.html', {'all_users':User.objects.all(), 'all_groups': Group.objects.all()})

@user_passes_test(lambda u: u.is_superuser)
def user_view(request, user_id):
    member = User.objects.get(id=user_id)
    if request.method == "POST":
            #something about editing the user?
        return render(request, 'accounts/sitemanager.html', {'all_users':User.objects.all()})
    else:
        return render(request, 'accounts/user_view.html', {'member':member})

@user_passes_test(lambda u: u.is_superuser)
def deactivate(request, user_id):
    member = User.objects.get(id=user_id)
    try:
        member.is_active=False
        member.save()
        messages.success(request, member.username + "'s account deactivated")
    except:
        messages.warning(request, member.username + "'s account still active")

    return render(request, 'accounts/user_view.html', {'member':member})

@user_passes_test(lambda u: u.is_superuser)
def activate(request, user_id):
    member = User.objects.get(id=user_id)
    try:
        member.is_active=True
        member.save()
        messages.success(request, member.username + "'s account reactivated")
    except:
        messages.warning(request, member.username + "'s account was not activated")

    return render(request, 'accounts/user_view.html', {'member':member})

@user_passes_test(lambda u: u.is_superuser)
def makeSiteManager(request, user_id):
    member = User.objects.get(id=user_id)
    try:
        member.is_superuser=True
        member.save()
        messages.success(request, member.username + " made into a site manager")
    except:
        messages.warning(request, member.username + " not made into a site manager")

    return render(request, 'accounts/user_view.html', {'member':member})

@user_passes_test(lambda u: u.is_superuser)
def unmakeSiteManager(request, user_id):
    member = User.objects.get(id=user_id)
    try:
        member.is_superuser=False
        member.save()
        messages.success(request, member.username + " is no longer a site manager")
    except:
        messages.warning(request, member.username + " is still a site manager")

    return render(request, 'accounts/user_view.html', {'member':member})

@user_passes_test(lambda u: u.is_superuser)
def groupsSM(request):
    if request.method == 'POST':
        if request.POST.get('user_name'):
            user_name = request.POST.get('user_name')
            group_name = request.POST.get('group_name')
            try:
                user = User.objects.get(username=user_name)
                group = Group.objects.get(name=group_name)
                user.groups.add(group)
                user.save()
                full_name = user.first_name + " " + user.last_name
                messages.success(request, full_name + " added to group!")
            except:
                messages.warning(request, 'User not added to group: Username not Found!')
        else:
            group_name = request.POST.get('group_name')
            try:
                newgroup = Group()
                newgroup.name = group_name
                newgroup.save()
                messages.success(request, 'Group Created.')
            except:
                messages.warning(request, 'Group Creation Failed. Group Already Exists.')

        return HttpResponseRedirect('/accounts/sitemanager')
    return render(request, 'accounts/sitemanager.html', {})
