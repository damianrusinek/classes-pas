import sys
import socket 
import asyncio

clients = []


def parse_recvd_data(data):
	""" Break up raw received data into messages, delimited
		by null byte """
	parts = data.split(b'\0')
	msgs = parts[:-1]
	rest = parts[-1]
	return (msgs, rest)


def prep_msg(msg):
	""" Prepare message """
	msg += '\0'
	return msg.encode('utf-8')


class ChatServerProtocol(asyncio.Protocol):
	""" Each instance of class represents a client and the socket
	connection to it. """

	def connection_made(self, transport):
		""" Called on instantiation, when new client connects """
		self.transport = transport
		self.addr = transport.get_extra_info('peername')
		self._rest = b''
		self.name = None
		clients.append(self)
		print('Connection from {}'.format(self.addr))
	
	def data_received(self, data):
		""" Handle data as it's received. Broadcast complete
		messages to all other clients """
		data = self._rest + data
		(msgs, rest) = parse_recvd_data(data)
		self._rest = rest
		for msg in msgs:
			msg = msg.decode('utf-8')
			if self.name is None:
				self.name = msg
			else:
				msg = '{}: {}'.format(self.name, msg)
				print(msg)
				msg = prep_msg(msg)
				for client in clients:
					client.transport.write(msg) # <-- non-blocking
		
	def connection_lost(self, ex):
		""" Called on client disconnect. Clean up client state """
		print('Client {} disconnected'.format(self.addr))
		clients.remove(self)

if __name__ == '__main__':
	if len(sys.argv) != 2:
		sys.stderr.write("usage: chat_server port\n")
		exit(1)

	try:
		port = int(sys.argv[1])
		assert port > 0
	except:
		sys.stderr.write("error: invalid port\n")
		exit(1)

	loop = asyncio.get_event_loop()
	# Create server and initialize on the event loop
	coroutine = loop.create_server(ChatServerProtocol, host='0.0.0.0', port=port)
	server = loop.run_until_complete(coroutine)
	# print listening socket info
	for socket in server.sockets:
		addr = socket.getsockname()
		print('Listening on {}'.format(addr))
	# Run the loop to process client connections
	loop.run_forever()