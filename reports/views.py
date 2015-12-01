from django.utils import timezone
from django.shortcuts import render, render_to_response
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from .forms import ReportForm, AttachmentForm
import re
from django.db.models import Q
from django.template import RequestContext
from .models import Report, Folder, Attachment
from django.contrib.auth.models import Group, User
from Crypto.Hash import MD5
from Crypto.Cipher import DES
from Crypto.Hash import SHA256
from django.core.mail import send_mail

@login_required
def reports(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        f = ReportForm(request.POST)
        # check whether it's valid:
        if f.is_valid():
            # Save the form data to the database.
            # But dont yet commit, we still have some data to add.
            report = f.save(commit=False)
            report.create_date = timezone.now()
            report.creator = request.user
            # NOW we can save
            report.save();

            folder = request.user.folder_set.get(label="Uncategorized")
            folder.reports.add(report)
            folder.save()

            # redirect to a new URL:
            messages.success(request, 'Report Created.')
            return HttpResponseRedirect('/')
        else:
            messages.warning(request, 'Report Not Created!')
            return render(request, 'reports/reports.html', {'report_form': f})
    # if a GET (or any other method) we'll create a blank form
    else:
        report_form = ReportForm()
        return render(request, 'reports/reports.html', {'report_form': report_form})

    return render(request, 'reports/reports.html')

@login_required
def folders(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        if not Folder.objects.filter(owner=request.user, label=request.POST['folder_name']):
            newfolder = Folder()
            newfolder.label= request.POST['folder_name']
            newfolder.owner = request.user
            newfolder.save()
            messages.success(request, 'Folder Created!')
            return HttpResponseRedirect('/')
        else:
           messages.warning(request, 'You already have a folder with that name!')
           return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')

@login_required
def attachments(request, report_id):
    if request.method == "POST":
        report = Report.objects.get(id=report_id)
        f = AttachmentForm(request.POST, request.FILES)
        # check whether it's valid:
        print('upload' in request.FILES)
        if f.is_valid():
            # Save the form data to the database.
            # But dont yet commit, we still have some data to add.
            attachment = f.save(commit=False)
            attachment.upload_date = timezone.now()
            attachment.report = report
            # NOW we can save
            attachment.save();

            h = MD5.new()
            chunk_size = 8192
            with open(attachment.upload.path, 'rb') as f:
                while True:
                    chunk = f.read(chunk_size)
                    if len(chunk) == 0:
                        break
                    h.update(chunk)
            attachment.key = h.hexdigest()
            attachment.save()

            messages.success(request, 'Attachment added!')
            return render(request, 'reports/read_report.html', {'report': report, "attachment_form": AttachmentForm()})
        else:
            messages.warning(request, 'Attachment failed to add!')
            return render(request, 'reports/read_report.html', {'report': report, "attachment_form": f})

@login_required
def delete_report(request, report_id):
    if Report.objects.filter(creator=request.user) or request.user.is_superuser:
        Report.objects.get(id=report_id).delete()
        messages.success(request, 'Report destroyed')
        if request.user.is_superuser:
            return HttpResponseRedirect('/accounts/sitemanager/')
        else:
            return HttpResponseRedirect('/')
    else:
        messages.warning(request, "Your report was not deleted.")
        if request.user.is_superuser:
            return HttpResponseRedirect('/accounts/sitemanager/')
        else:
            return HttpResponseRedirect('/')

@login_required
def edit_report(request, report_id):
    report = Report.objects.get(id=report_id)
    if request.method == 'POST':
        form = ReportForm(request.POST, instance=report)
        if form.is_valid():
            report = form.save(commit=True)
            messages.success(request, 'Report Edited.')
            return HttpResponseRedirect('/')
        else:
            form = ReportForm(instance=report)
            messages.warning(request, 'Report Not Edited!')
            #return HttpResponseRedirect('/')
    else:
        form = ReportForm(instance=report)

    return render(request, 'reports/edit_report.html', {'report_form': form,'report_id':report_id})

@login_required
def edit_folder(request, folder_id):
    if request.method == 'POST': #rename folder
        if not Folder.objects.filter(owner=request.user, label=request.POST['folder_name']):
            Folder.objects.filter(pk=folder_id).update(label=request.POST['folder_name'])
            messages.success(request, 'Folder Renamed!')
            return HttpResponseRedirect('/')
        else:
           messages.warning(request, 'You already have a folder with that name!')
           return render(request, 'reports/rename_folder.html')
    if(request.GET.get('dlt')): #button pressed, delete folder
        if Folder.objects.filter(owner=request.user):
            Folder.objects.get(id=folder_id).delete()
            messages.success(request, 'Folder destroyed')
            return HttpResponseRedirect('/')
        else:
            messages.warning(request, "Your folder is still among us.")
            return HttpResponseRedirect('/')
    f = Folder.objects.get(pk=folder_id)
    return render(request, 'reports/rename_folder.html', {'folder_id':folder_id, 'labeled':f.label})

@login_required
def move(request):
    if request.method == 'POST':
        if Folder.objects.get(id = request.POST['move_from']):
            start = Folder.objects.get(id=request.POST['move_from'])
            end = Folder.objects.get(id=request.POST['move_to'])

            if start == end :
                messages.warning(request, "You cannot move reports to their current folder!")
                return HttpResponseRedirect('/')
            else:
                rep = Report.objects.get(id = request.POST['currep'])
                Folder.objects.get(id = request.POST['move_to']).reports.add(rep)
                Folder.objects.get(id = request.POST['move_from']).reports.remove(rep)
                messages.success(request, 'Folder successfully moved!')
                return HttpResponseRedirect('/')


@login_required
def read_report(request, report_id):
    if request.method == "POST":
        report = Report.objects.get(id=report_id)
        f = AttachmentForm(request.POST, request.FILES)
        # check whether it's valid:
        # print('upload' in request.FILES)
        # if f.is_valid():
        #     # Save the form data to the database.
        #     # But dont yet commit, we still have some data to add.
        #     attachment = f.save(commit=False)
        #     attachment.upload_date = timezone.now()
        #     attachment.report = report
        #     # NOW we can save
        #     attachment.save();
        #     messages.success(request, 'Attachment added!')
        #     return render(request, 'reports/read_report.html', {'report': report, "attachment_form": AttachmentForm()})
        # else:
        #     messages.warning(request, 'Attachment failed to add!')
        #     return render(request, 'reports/read_report.html', {'report': report, "attachment_form": f})
    else:
        report = Report.objects.get(id=report_id)
        if Report.objects.filter(creator=request.user):
            report.save()
            attachment_form = AttachmentForm()
            return render(request, 'reports/read_report.html', {'report': report, "attachment_form": attachment_form})
        else:
            messages.warning(request, "Couldn't read your report")
            return HttpResponseRedirect('/')

@login_required
def delete_attachment(request, attachment_id):
    try:
        attachment = Attachment.objects.get(id=attachment_id)
        os.remove(attachment.upload.path)
        report = attachment.report
        attachment.delete()
        messages.success(request, "Attachment Deleted")
        return render(request, 'reports/read_report.html', {'report': report, "attachment_form": AttachmentForm()})
    except:
        messages.warning(request, "ERROR: Attachment Not Deleted!")
        return HttpResponseRedirect('/')

@login_required
def search(request):
    query_string = ''
    found_entries = None
    found_entries_two = None
    if ('q' in request.GET) and request.GET['q'].strip():
        if 'id_creator' is True:
            query_string = request.GET['q']
            entry_query = get_query(query_string,  ['creator'])
        elif 'id_attach' is True :
            query_string = request.GET['q']
            entry_query = get_query(query_string,  ['name'])
        elif 'id_report' is True :
            query_string = request.GET['q']
            entry_query = get_query(query_string,  ['title'])
        elif 'id_folder' is True:
            query_string = request.GET['q']
            entry_query = get_query(query_string,  ['label'])
        elif'id_folder' and 'id_report' and 'id_attach' and 'id_creator' is not True:
            query_string = request.GET['q']
            entry_query = get_query(query_string,  ['title', 'description',])
        found_entries = Report.objects.filter(entry_query)
        query_string = request.GET['q']
        if "AND" in query_string:
            query_string = request.GET['q'].replace('AND','')

        entry_query = get_query(query_string, ['title', 'description', ])
        all_entries = Report.objects.filter(entry_query)

        if "OR" in query_string:
            query_string = request.GET['q'].split('OR')
            query_string_one = query_string[0]
            query_string_two = query_string[1]
            entry_query = get_query(query_string_one, ['title', 'description', ])
            entry_query_two = get_query(query_string_two, ['title', 'description', ])
            found_entries = Report.objects.filter(entry_query)
            found_entries_two = Report.objects.filter(entry_query_two)
            all_entries = found_entries | found_entries_two

    if ('and' in 'q'):
        print("hello!")
    if('or' in 'q'):
        print('hello!')

    return render_to_response('reports/search_results.html',
                              {'query_string': query_string, 'found_entries': all_entries},
                              context_instance=RequestContext(request))

def normalize_query(query_string,
    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
    normspace=re.compile(r'\s{2,}').sub):
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]

def get_query(query_string, search_fields):
    ''' Returns a query, that is a combination of Q objects. That combination
        aims to search keywords within a model by testing the given search fields.

    '''
    query = None # Query to search for every search term
    terms = normalize_query(query_string)

    for term in terms:
        or_query = None # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query


def public(request):
    reports = Report.objects.filter(public=True)
    return render(request, 'reports/public.html', {'reports': reports})

@login_required
def contributors(request, report_id):
    if request.method == 'POST':
        group_name = request.POST.get('group_name')
        group = Group.objects.get(name=group_name)
        report = Report.objects.get(id=report_id)
        users = group.user_set.all()
        author = request.user
        for user in users:
            if author != user:
                folder = user.folder_set.get(label="Shared With Me")
                folder.reports.add(report)
                folder.save()

        messages.success(request, "Added group members as contributors!")

    return HttpResponseRedirect('/')

@login_required
def encrypt_attachment(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        f = AttachmentForm(request.POST)
        contributor = request.POST.get('contributor_name')
        report = f.save(commit=False)
        report.creator = request.user
        report.save();
        # check whether it's valid:
        if f.is_valid():
            # Save the form data to the database.
            # But dont yet commit, we still have some data to add.
            attachment = Attachment()
            attachment.upload = f.cleaned_data['upload']
            if attachment.encrypted:
                thehash = SHA256.new(os.urandom(4))
                hashstring = thehash.digest()[0:8]
                attachment.key = str(hashstring)
                des = DES.new(hashstring, DES.MODE_ECB)
                text = str.encode(str(f.cleaned_data['upload']))
                while len(text) % 8 != 0:
                    text += b'\0'
                attachment.content = str(des.encrypt(text))
                send_mail('[SecureShare] New Encrypted Attachment Key',
                 'The DES key for this message is '+attachment.key+'.',
                 'secureshare21@yahoo.com', [report.creator.email], fail_silently=False)
                messages.success('email with key sent to ' + 'report.creator.email')

    return HttpResponseRedirect('/')



############################################## API VIEWS ARE BELOW ##
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from .serializers import FolderSerializer, ReportSerializer, AttachmentInfoSerializer
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.core.files import File
from django.http import StreamingHttpResponse
from django.core.servers.basehttp import FileWrapper
import mimetypes
import os

@api_view(['GET'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def api_available_reports(request):
    if request.method == 'GET':
        folders = request.user.folder_set
        serializer = FolderSerializer(folders, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def api_public_reports(request):
    if request.method == 'GET':
        reports = Report.objects.filter(public=True)
        serializer = ReportSerializer(reports, many=True)
        return Response(serializer.data)

@api_view(['GET'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
def api_download_attachment(request, attachment_id):
    thefile = Attachment.objects.get(id=attachment_id)
    if not thefile.has_access(request.user):
        return HttpResponse("denied")
    wrapper = FileWrapper(open(thefile.upload.path, 'rb'))
    thetype = ""
    try:
        thetype = mimetypes.guess_type(thefile.filename())[0] + "; charset=binary"
    except:
        thetype = "application/bin; charset=binary"
    response = HttpResponse(wrapper, content_type=thetype)
    response['Content-Disposition'] = "attachment; filename=file"
    return response

@api_view(['POST'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def api_add_report(request):
    if request.method == 'POST':
        serializer = AttachmentInfoSerializer(data=request.data)
        if serializer.is_valid():
            a = serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
