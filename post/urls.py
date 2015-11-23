from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^new/$', views.new, name='new'),
    url(r'^inbox/$', views.inbox, name='inbox'),
    url(r'^(?P<message_id>[0-9]+)/delete/$', views.delete, name='delete'),
    url(r'^(?P<message_id>[0-9]+)/read/$', views.read, name='read'),
]
