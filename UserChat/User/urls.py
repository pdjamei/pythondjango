from django.conf.urls import url
from User.views import UserDetailView, UserListView

urlpatterns = [
	url('^user/(?P<pk>[\w]+)/$', UserDetailView.as_view(), name='user-detail'),
	url('^user/$', UserListView.as_view(), name='user-list'),
]
