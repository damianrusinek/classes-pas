from optparse import OptionParser
import socket, threading, logging, sys, struct
from os import path
import messages as mmsg

sys.path.append(path.join(path.sep, 'opt', 'knxmap'))
from libknxmap import messages as msg
from libknxmap.data import constants

KNX_STATUS_NAMES = {v: k for k, v in constants.KNX_STATUS_CODES.items()}

DEFAULT_PORT = 3671
EMPTY_CONNECTION = {
	'address': None,
	'sequence': 0,
}

GROUP_VALUE = 0
MONITOR_PORT = 3333

class KNXServer():

	def __init__(self, group_address, port, options):
		self.port = port
		self.group_address = tuple(map(int, group_address.split('/')))
		self.options = options
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.connections = {}
		self.next_communication_channel = 1
	
	def parse_knx_message(self, data):
		try:
			_, _, message_type = struct.unpack('>BBH', data[:4])
			message_type = int(message_type)
		except struct.error as e:
			logging.exception(e)
			return
		except ValueError as e:
			logging.exception(e)
			return
		
		if message_type == msg.KNX_MESSAGE_TYPES.get('DESCRIPTION_REQUEST'):
			logging.debug('Parsing KnxDescriptionRequest')
			return msg.KnxDescriptionRequest(data)
		elif message_type == msg.KNX_MESSAGE_TYPES.get('CONNECT_REQUEST'):
			logging.debug('Parsing KnxConnectRequest')
			return msg.KnxConnectRequest(data)
		elif message_type == msg.KNX_MESSAGE_TYPES.get('DISCONNECT_REQUEST'):
			logging.debug('Parsing KnxDisconnectRequest')
			return msg.KnxDisconnectRequest(data)
		else:
			m = msg.parse_message(data)
		return m
	
	def parse_group_address_integer(self, addr):
			return addr >> 11 & 0x1f, addr >> 8 & 0x7, addr & 0xff

	def create_new_communication_channel(self, client_addr):
		status = KNX_STATUS_NAMES['E_NO_ERROR']
		i = 0
		while i < 256 and self.next_communication_channel in self.connections:
			i += 1
			self.next_communication_channel = (self.next_communication_channel + 1) % 256
			if self.next_communication_channel == 0:
				self.next_communication_channel = 1
		if i >= 256:
			logging.error("No connection channels left.")
			status = KNX_STATUS_NAMES['E_NO_MORE_CONNECTIONS']
			communication_channel = 0
		else:			
			communication_channel = self.next_communication_channel
			self.connections[communication_channel] = EMPTY_CONNECTION
			self.connections[communication_channel]['address'] = client_addr
		return status, communication_channel

	def get_next_sequence(self, communication_channel, current_sequence=None):
		if current_sequence is not None:
			self.connections[communication_channel]['sequence'] = current_sequence
		self.connections[communication_channel]['sequence'] += 1
		return self.connections[communication_channel]['sequence']
		
	def remove_communication_channel(self, communication_channel):
		del self.connections[communication_channel]
			
	def is_communication_channel_active(self, communication_channel):
		return communication_channel is not None and communication_channel in self.connections
	
	def handle_request(self, data, client_addr):
		m = self.parse_knx_message(data)
		logging.info('Received message from client %s: %s', client_addr, m.__class__.__name__)
		
		if isinstance(m,msg.KnxDescriptionRequest):
			logging.debug('KnxDescriptionRequest')
			resp = mmsg.KnxDescriptionResponse(request=m)
			resp.pack_knx_message()
			logging.debug("Sending KnxDescriptionResponse")
			self.sock.sendto(resp.get_message(), client_addr)
		
		elif isinstance(m,msg.KnxConnectRequest):
			logging.debug('KnxConnectRequest')
			status, communication_channel = self.create_new_communication_channel(client_addr)
			logging.debug("Preparing KnxConnectResponse")
			resp = mmsg.KnxConnectResponse(request=m, communication_channel=communication_channel, status=status)
			resp.pack_knx_message()
			logging.debug("Sending KnxConnectResponse")
			self.sock.sendto(resp.get_message(), client_addr)
			
		elif isinstance(m,msg.KnxDisconnectRequest):
			logging.debug('KnxDisconnectRequest')
			communication_channel = m.body['communication_channel_id']
			status = KNX_STATUS_NAMES['E_NO_ERROR'] if self.is_communication_channel_active(communication_channel) else KNX_STATUS_NAMES['E_CONNECTION_ID']
			if self.is_communication_channel_active(communication_channel):
				self.remove_communication_channel(communication_channel)
			resp = mmsg.KnxDisconnectResponse(communication_channel=communication_channel, status=status, request=m)
			resp.pack_knx_message()
			logging.debug("Sending KnxDisconnectResponse")
			self.sock.sendto(resp.get_message(), client_addr)
			
		elif isinstance(m,msg.KnxConnectionStateRequest):
			logging.debug('KnxConnectionStateRequest')
			communication_channel = m.body['communication_channel_id']
			status = KNX_STATUS_NAMES['E_NO_ERROR'] if self.is_communication_channel_active(communication_channel) else KNX_STATUS_NAMES['E_CONNECTION_ID']
			resp = mmsg.KnxConnectionStateResponse(status=status, communication_channel=communication_channel, request=m)
			resp.pack_knx_message()
			logging.debug("Sending KnxConnectionStateResponse")
			self.sock.sendto(resp.get_message(), client_addr)
		
		elif isinstance(m,msg.KnxTunnellingAck):
			logging.debug('KnxTunnellingAck')
		
		elif isinstance(m,msg.KnxTunnellingRequest):
			logging.debug('KnxTunnellingRequest')
			communication_channel = m.body['communication_channel_id']
			if not self.is_communication_channel_active(communication_channel):
				return

			resp = mmsg.KnxTunnellingAck(request=m, communication_channel=communication_channel, sequence_count=m.body['sequence_counter'])
			resp.pack_knx_message()
			logging.debug("Sending KnxConnectionStateResponse")
			self.sock.sendto(resp.get_message(), client_addr)

			knx_destination = '/'.join(map(str, self.parse_group_address_integer(m.body['cemi']['knx_destination'])))

			# Send confirmation
			if m.body['cemi']['message_code'] == constants.CEMI_MSG_CODES['L_Data.req']:
				resp = mmsg.KnxTunnellingRequestConfirmation(request=m, communication_channel=communication_channel, 
					sequence_count=self.get_next_sequence(communication_channel,m.body['sequence_counter']), sockname=client_addr,
					knx_source='0.0.0', knx_destination=knx_destination)
				logging.debug("Sending KnxTunnellingRequestConfirmation")
				self.sock.sendto(resp.get_message(), client_addr)

			#Send indicator
			if self.group_address == self.parse_group_address_integer(m.body['cemi']['knx_destination']):
				global GROUP_VALUE
				GROUP_VALUE = m.body['cemi']['apci']['data']
				resp = mmsg.KnxTunnellingRequestIndicator(request=m, communication_channel=communication_channel, 
					sequence_count=self.get_next_sequence(communication_channel,m.body['sequence_counter']), sockname=client_addr,
					knx_source='1.1.1', knx_destination=knx_destination)
				logging.debug("Sending KnxTunnellingRequestIndicator")
				self.sock.sendto(resp.get_message(), client_addr)
			
		else:
			logging.error('Unknown knx message.')
			
	def start(self):
		addr = ('0.0.0.0', self.port)
		self.sock.bind(addr)
		logging.debug("Server started at %s:%d" % addr)
    
		while True:
			data, client_addr = self.sock.recvfrom(1024)
			t = threading.Thread(target=self.handle_request, args=(data, client_addr))
			t.start()

def group_value_monitor():
	global GROUP_VALUE
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	addr = ('0.0.0.0', MONITOR_PORT)
	sock.bind(addr)
	logging.debug("Monitor started at %s:%d" % addr)
  
	while True:
		data, client_addr = sock.recvfrom(1)
		logging.debug("Received monitor request from %s:%d" % client_addr)
		sock.sendto(bytes(map(ord, list(str(GROUP_VALUE)))), client_addr)

def main():
	usage = "usage: %prog [options] [port] group_address"
	parser = OptionParser(usage=usage)
	parser.add_option('-v', '--verbose', action='store_true', dest='verbose')
	(options, args) = parser.parse_args()
	if len(args) == 2:
		try:
			port = int(args[0])
		except ValueError:
			parser.error("port must be an integer")

		if len(args[1].split('/')) != 3:
			parser.error("invalid group_address format")
		else:
			for i in args[1].split('/'):
				try:
					if len(i) != 1:
						raise ValueError()
					port = int(i)
				except ValueError:
					parser.error("group_address can consist of integers only")
		group_address = args[1]
	elif len(args) == 1:
		port = DEFAULT_PORT
		if len(args[0].split('/')) != 3:
			parser.error("invalid group_address format")
		else:
			for i in args[0].split('/'):
				try:
					if len(i) != 1:
						raise ValueError()
					int(i)
				except ValueError:
					parser.error("group_address can consist of integers only")
		group_address = args[0]
	else:
		parser.error("group_address is required")
	
	if options.verbose:
		logging.getLogger().setLevel(logging.DEBUG)
	
	# Monitor
	t = threading.Thread(target=group_value_monitor)
	t.start()

	server = KNXServer(group_address, port, options)
	server.start()

if __name__ == '__main__':
	main()
	
	