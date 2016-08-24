from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.users, name='users'),
    url(r'^create/$', views.create, name='create'),
    url(r'^edit/(?P<user_id>[0-9]+)$', views.edit, name='edit'),
    url(r'^courses/$', views.courses, name='courses'),
]