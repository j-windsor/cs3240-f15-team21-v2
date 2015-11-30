from django import forms
from .models import Report, Folder, Attachment, Contributor

class ReportForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}))
    public = forms.BooleanField(required=False)
    class Meta:
        model = Report
        fields = ('title', 'description', 'public')

class AttachmentForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    upload = forms.FileField()
    class Meta:
        model = Attachment
        fields = ('name', 'upload')

class ContributorForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    class Meta:
        model = Contributor
        fields = ('name',)
