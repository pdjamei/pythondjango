from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
# Create your views here.

class UserDetailView(DetailView):
	model = User



class UserListView(ListView):
	model = User