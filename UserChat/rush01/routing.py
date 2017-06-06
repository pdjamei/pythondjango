from channels.routing import include
from message.routing import list_routing

channel_routing = [
		include(list_routing)
]
