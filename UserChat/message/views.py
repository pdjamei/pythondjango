from django.shortcuts import render
from django.views.generic.list import ListView
from message.models import Message
# Create your views here.

class HistoriqueView(ListView):
	model = Message