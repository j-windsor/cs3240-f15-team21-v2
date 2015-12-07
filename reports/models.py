from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import os

class Report(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length = 200)
    create_date = models.DateTimeField('date created')
    public = models.BooleanField(default=True)
    creator = models.ForeignKey(User)
    #encrypted = models.BooleanField(default=False)
    def get_creator(self):
        return str(self.creator)
    def is_public(self):
        return self.public

class Folder(models.Model):
    label = models.CharField(max_length=30)
    reports = models.ManyToManyField(Report)
    owner = models.ForeignKey(User)
    def __str__(self):
        return self.label

def get_upload_file_name(instance,filename):
    return "uploaded_files/%s_%s" % (str(timezone.now()).replace('.','_'),filename)

class Attachment (models.Model):
    name = models.CharField(max_length=30)
    upload = models.FileField(upload_to=get_upload_file_name)
    key = models.CharField(max_length=100)
    encrypted = models.BooleanField(default=False)
    upload_date = models.DateTimeField('date uploaded', auto_now_add=True)
    report = models.ForeignKey(Report)
    def __str__(self):
        return self.name
    def filename(self):
        return os.path.basename(self.upload.path)
    def has_access(self, user):
        retval = False
        try:
            for folder in user.folder_set.all():
                for report in folder.reports.all():
                    if self in report.attachment_set.all():
                        retval = True
            if self.report.public = True:
                retval = True
        except:
            pass
        return retval

class Contributor (models.Model):
    name = models.CharField(max_length=30)
    def __str__(self):
        return self.name
