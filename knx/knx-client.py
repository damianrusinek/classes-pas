import socket, struct, sys, math


class KnxMessage:

	def __init__(self, message=None, **kwargs):
		
		if message is not None:
			self._unpack_from_message(message)
		else:
			self._unpack_from_kwargs(**kwargs)

	def _unpack_from_message(self, message):
		service_type = struct.unpack('>H', message[2:4])[0]
		if service_type != self.get_service_type():
			print('Protocol error')
			exit(2)

		self._unpack_body_from_message(message)

	def _unpack_from_kwargs(self, **kwargs):
		raise NotImplementedError()
		
	def get_service_type(self):
		raise NotImplementedError()

	def build_header(self, body_size):
		total_size = body_size + 6
		total_size_bytes = bytes([0x00,total_size]) if total_size < 252 else bytes([0xff,total_size - 252])
		return bytes.fromhex('0610') + struct.pack('>H', self.get_service_type()) + total_size_bytes

	def build_body(self):
		raise NotImplementedError()

	def get_bytes(self):
		body = self.build_body()
		return self.build_header(len(body)) + body


class DescriptionRequestMessage(KnxMessage):

	def __init__(self, message=None, sock_addr=None):
		super(DescriptionRequestMessage, self).__init__(message=message, sock_addr=sock_addr)

	def _unpack_from_kwargs(self, sock_addr=None):
		self.sock_addr = sock_addr

	def get_service_type(self):
		return 0x0203

	def build_body(self):
		return bytes([0x08, 0x01]) + bytes(list(map(int, self.sock_addr[0].split('.')))) + struct.pack('>H', self.sock_addr[1])


class DescriptionResponseMessage(KnxMessage):

	def __init__(self, message=None):
		super(DescriptionResponseMessage, self).__init__(message=message)
	
	def _unpack_body_from_message(self, message):
		self.name = ''
		i = 30
		while message[i] != 0:
			self.name += chr(message[i])
			i += 1

	def get_service_type(self):
		return 0x0204


class ConnectRequestMessage(KnxMessage):

	def __init__(self, message=None):
		super(ConnectRequestMessage, self).__init__(message=message)

	def _unpack_from_kwargs(self):
		pass

	def get_service_type(self):
		return 0x0205

	def build_body(self):
		hpai = bytes([0x08, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
		return hpai + hpai + bytes([0x04,0x04,0x02,0x00])


class ConnectResponseMessage(KnxMessage):

	def __init__(self, message=None):
		super(ConnectResponseMessage, self).__init__(message=message)
	
	def _unpack_body_from_message(self, message):
		self.communication_channel_id = message[6]

	def get_service_type(self):
		return 0x0206


class TunnellingRequestMessage(KnxMessage):

	def __init__(self, message=None, communication_channel_id=None, sequence_counter=0, cemi=None):
		super(TunnellingRequestMessage, self).__init__(message=message, 
			communication_channel_id=communication_channel_id, 
			sequence_counter=sequence_counter, cemi=cemi)

	def _unpack_from_kwargs(self, cemi=None, communication_channel_id=None, sequence_counter=0):
		self.communication_channel_id = communication_channel_id
		self.sequence_counter = sequence_counter
		self.cemi = cemi

	def _unpack_body_from_message(self, message):
		self.communication_channel_id = message[7]
		self.sequence_counter = message[8]
		self.cemi = {
			'code': message[10],
			'source': message[14:15],
			'destination': message[16:17],
			'apci': message[19] & 0x03 << 2 
		}

		size = message[18]
		data = message[20] & 0x3f
		if size > 1:
			i = 0
			while i < size:
				data = data << 8
				data += message[21 + i]
				i += 1
		self.cemi['data'] = data

	def get_service_type(self):
		return 0x0420

	def build_body(self):
		apci_size = math.ceil((len(bin(self.cemi['data'])[2:]) - 6) / 8.0) + 1
		apci_data = (self.cemi['apci'] << 6) + (self.cemi['data'] >> 8 * (apci_size-1)) 
		apci_data_additional = self.cemi['data'] - (self.cemi['data'] >> 8 * (apci_size-1) << 8 * (apci_size-1))
		apci_data_additional_bytes = apci_data_additional.to_bytes(apci_size-1, 'big')
		return bytes([0x04, self.communication_channel_id, self.sequence_counter, 0x00, self.cemi['code'], 0x00, 0xbc, 0xe0]) \
			+ self.cemi['source'] + self.cemi['destination'] + bytes([apci_size]) + struct.pack('>H', apci_data) \
			+ apci_data_additional_bytes


class TunnellingAckMessage(KnxMessage):

	def __init__(self, message=None, communication_channel_id=None, sequence_counter=0):
		super(TunnellingAckMessage, self).__init__(message=message, 
			communication_channel_id=communication_channel_id, sequence_counter=sequence_counter)
	
	def _unpack_from_kwargs(self, communication_channel_id=None, sequence_counter=0):
		self.communication_channel_id=communication_channel_id
		self.sequence_counter=sequence_counter

	def _unpack_body_from_message(self, message):
		pass

	def build_body(self):
		return bytes([0x04, self.communication_channel_id, self.sequence_counter, 0x00])

	def get_service_type(self):
		return 0x0421


def parse_group_address(addr):
	try:
		parts = list(map(int, addr.split('/')))
		if len(parts) != 3:
			return None
		return '/'.join(map(str, parts))
	except:
		return None

def group_address_to_bytes(addr):
	parts = list(map(int, addr.split('/')))
	return bytes([((parts[0] & 0x1f) << 3) + (parts[1] & 0x7), parts[2] & 0xff])

def individual_address_to_bytes(addr):
	parts = list(map(int, addr.split('.')))
	return bytes([((parts[0] & 0x0f) << 4) + (parts[1] & 0x0f), parts[2] & 0xff])   	

def parse_ip(ip):
	try:
		parts = list(map(int, ip.split('.')))
		if len(parts) != 4:
			return None
		for i in parts:
			if i < 0 or i > 255:
				return None
		return '.'.join(map(str, parts))
	except:
		return None

def parse_port(port):
	try:
		port = int(port)
		if port >= 2**16 or port < 0:
			return None
		return port
	except:
		return None

def parse_value(value):
	try:
		value = int(value)
		if value not in [0,1,11,257]:
			return None
		return value
	except:
		return None

def usage():
	print("usage: %s <ip> <port> <address> <value>" % sys.argv[0])

if __name__ == '__main__':

	if len(sys.argv) != 5:
		usage()
		exit(1)

	ip = parse_ip(sys.argv[1])
	port = parse_port(sys.argv[2])
	address = parse_group_address(sys.argv[3])
	value = parse_value(sys.argv[4])

	if None in [ip, port, address, value]:
		usage()
		exit(1)

	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	print('Connecting to', ip, port, '...')
	s.connect((ip, port))
	print('Connected.')

	print('Sending Description Request.')
	s.send(DescriptionRequestMessage(sock_addr=s.getsockname()).get_bytes())

	message = s.recv(1024)
	print('Received Description Response.')
	print('KNXnet/IP name:', DescriptionResponseMessage(message=message).name)

	print('Sending Connection Request.')
	s.send(ConnectRequestMessage().get_bytes())

	message = s.recv(1024)
	print('Received Connection Response.')
	communication_channel_id = ConnectResponseMessage(message=message).communication_channel_id
	print('Communication Channel ID:', communication_channel_id)

	print('Sending Tunneling Request.')
	APCI_WRITE = 2
	cemi = {
			'code': 0x11,
			'source': individual_address_to_bytes('0.0.0'),
			'destination': group_address_to_bytes(address),
			'apci': APCI_WRITE,
			'data': value 
		}
	s.send(TunnellingRequestMessage(communication_channel_id=communication_channel_id, sequence_counter=0, cemi=cemi).get_bytes())
	
	message = s.recv(1024)
	print('Received Tunnelling Ack.')
	TunnellingAckMessage(message=message)	

	message = s.recv(1024)
	print('Received Tunnelling Request (confirmation).')
	print('Message code:', hex(TunnellingRequestMessage(message=message).cemi['code']))

	print('Sending Tunneling Ack.')
	s.send(TunnellingAckMessage(communication_channel_id=communication_channel_id).get_bytes())

	message = s.recv(1024)
	print('Received Tunnelling Request (indication).')
	print('Message code:', hex(TunnellingRequestMessage(message=message).cemi['code']))

	print('Sending Tunneling Ack.')
	s.send(TunnellingAckMessage(communication_channel_id=communication_channel_id).get_bytes())

	print('Closing connection...')
	s.close()
	print('Closed.')

	print('Checking value...')
	MONITOR_PORT = 3333
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect((ip, MONITOR_PORT))
	s.send(b'')
	print('Value:', s.recv(100).decode('utf8'))
	s.close()
		
	
