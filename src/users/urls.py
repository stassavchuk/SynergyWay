from django.conf.urls import url

from .views import CreateUserView, CoursesView, EditUserView, UserListView

urlpatterns = [
    url(r'^$', UserListView.as_view(), name='users'),
    url(r'^create/$', CreateUserView.as_view(), name='create'),
    url(r'^edit/(?P<user_id>[0-9]+)$', EditUserView.as_view(), name='edit'),
    url(r'^courses/$', CoursesView.as_view(), name='courses'),
]
