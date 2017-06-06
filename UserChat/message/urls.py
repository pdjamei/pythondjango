from django.conf.urls import url
from message.views import HistoriqueView

urlpatterns = [
	url('', HistoriqueView.as_view(), name='historique'),
]
