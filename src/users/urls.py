from django.conf.urls import url

from .views import CreateUserView

urlpatterns = [
    # url(r'^$', views.users, name='users'),
    url(r'^create/$', CreateUserView.as_view(), name='create'),
    # url(r'^edit/(?P<user_id>[0-9]+)$', views.edit, name='edit'),
    # url(r'^courses/$', views.courses, name='courses'),
]