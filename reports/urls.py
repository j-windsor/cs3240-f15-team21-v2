from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^reports/$', views.reports, name='reports'),
    url(r'^folders/$', views.folders, name='folders'),
    url(r'^search_reports/$', views.search, name = 'search'),
    url(r'^attachments/$', views.attachments, name='attachments'),
    url(r'^(?P<report_id>[0-9]+)/contributors/$', views.contributors, name='contributors'),
    url(r'^public/$', views.public, name='public'),
    url(r'^(?P<report_id>[0-9]+)/edit_report/$', views.edit_report, name='edit_report'),
    url(r'^(?P<report_id>[0-9]+)/delete_report/$', views.delete_report, name='delete_report'),
    url(r'^(?P<folder_id>[0-9]+)/edit_folder/$', views.edit_folder, name='edit_folder'),
    url(r'^move/$', views.move, name='move'),
    url(r'^(?P<report_id>[0-9]+)/attachments/$', views.attachments, name='attachments'),
    url(r'^(?P<report_id>[0-9]+)/read_report/$', views.read_report, name='read_report'),
    url(r'^(?P<attachment_id>[0-9]+)/delete_attachment/$', views.delete_attachment, name='delete_attachment'),
    url(r'^api_available_reports/$', views.api_available_reports, name='api_available_reports'),
    url(r'^api_public_reports/$', views.api_public_reports, name='api_public_reports'),
    url(r'^(?P<attachment_id>[0-9]+)/download_attachment/$', views.api_download_attachment, name='api_download_attachment'),
]
