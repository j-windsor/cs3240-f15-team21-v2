from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^groups/$', views.groups, name='groups'),
    url(r'^sitemanager/$', views.sitemanager, name='sitemanager'),
    url(r'^(?P<user_id>[0-9]+)/user_view/$', views.user_view, name='user_view'),
    url(r'^(?P<user_id>[0-9]+)/deactivate/$', views.deactivate, name='deactivate'),
    url(r'^(?P<user_id>[0-9]+)/activate/$', views.activate, name='activate'),
    url(r'^(?P<user_id>[0-9]+)/makeSiteManager/$', views.makeSiteManager, name='makeSiteManager'),

]
