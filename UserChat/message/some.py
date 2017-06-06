from message.models import Message
from django.contrib.auth.models import User
from channels import Group
from channels.sessions import channel_session

@channel_session
def ws_connect(message):
	print('Connected')
	message.channel_session['room'] = 'shared_conv'
	Group('shared_conv').add(message.reply_channel)
	Group('shared_conv').send({'text': "New connexion"})

@channel_session
def ws_message(message):
	m = message.content['text']
	print('New_message :', m)
	response = {
	'text': m,
	}
	user1= User.objects.get(username="toto")
	user2= User.objects.get(username="pdjamei")
	Message.objects.create(target=user1,sender=user2,content=m)
	room = message.channel_session['room']
	Group(room).send(response)

@channel_session
def ws_disconnect(message):
	print('Disco')
	room = message.channel_session['room']
	Group(room).discard(message.reply_channel)