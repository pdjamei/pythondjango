from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.

class Message(models.Model):

	date = models.DateTimeField(default=timezone.now)
	sender = models.ForeignKey(User, related_name="sender", on_delete=models.CASCADE)
	target = models.ForeignKey(User, related_name="target", on_delete=models.CASCADE)
	content = models.TextField()