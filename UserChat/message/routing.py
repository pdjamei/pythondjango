from channels.routing import route
from .some import ws_connect, ws_disconnect, ws_message

list_routing = [
	route("websocket.connect", ws_connect),
	route("websocket.disconnect", ws_disconnect),
	route("websocket.receive", ws_message),
]
