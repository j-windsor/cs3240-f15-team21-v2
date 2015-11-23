from django.shortcuts import render
from reports.models import Report, Folder

# Create your views here.

def index(request):
    return render(request, 'master/index.html', {})
