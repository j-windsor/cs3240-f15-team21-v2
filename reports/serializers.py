from rest_framework import serializers
from .models import Report, Folder, Attachment


class AttachmentInfoSerializer(serializers.ModelSerializer):
    upload = serializers.FileField(use_url=True)
    class Meta:
        model = Attachment
        fields = ('name', 'upload', 'encrypted', 'upload_date', 'id', 'report', 'key')

class ReportSerializer(serializers.ModelSerializer):
    attachment_set = AttachmentInfoSerializer(many=True)
    class Meta:
        model = Report
        fields = ('title', 'description', 'create_date', 'id', 'attachment_set')

class FolderSerializer(serializers.ModelSerializer):
    reports = ReportSerializer(many=True)
    class Meta:
        model = Folder
        fields = ('label', 'reports')
