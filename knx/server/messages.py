import sys, struct
from os import path

sys.path.append(path.join(path.sep, 'opt', 'knxmap'))
from libknxmap import messages as msg


class KnxDescriptionResponse(msg.KnxDescriptionResponse):

	def __init__(self, message=None, request=None):
		self.request = request
		super(KnxDescriptionResponse, self).__init__(message=message)

	def _pack_knx_body(self):
		self.body = bytearray.fromhex('3601020000000000b8874bdf6e7fe000170c0242ac1100026b6e786420706173000000000000000'+
		'00000000000000000000000000000000000000a020201030104010501')
		return self.body


class KnxConnectResponse(msg.KnxConnectResponse):

	def __init__(self, message=None, request=None, communication_channel=None, status=0):
		self.request = request
		self.communication_channel = communication_channel
		self.status = status
		super(KnxConnectResponse, self).__init__(message=message)

	def _pack_knx_body(self):
		self.body = bytearray.fromhex(('%02x' % self.communication_channel) + ('%02x' % self.status) + '080100000000000004040000')
		return self.body


class KnxDisconnectResponse(msg.KnxDisconnectResponse):

	def __init__(self, message=None, request=None, communication_channel=1, status=0):
		self.request = request
		self.communication_channel = communication_channel
		self.status = status
		super(KnxDisconnectResponse, self).__init__(message=message, communication_channel=communication_channel)

	def _pack_knx_body(self):
		self.body = bytearray.fromhex(('%02x' % self.communication_channel) + ('%02x' % self.status))
		return self.body


class KnxConnectionStateResponse(msg.KnxConnectionStateResponse):

	def __init__(self, message=None, request=None, communication_channel=1, status=0):
		self.request = request
		self.status = status
		self.communication_channel = communication_channel
		super(KnxConnectionStateResponse, self).__init__(message=message, communication_channel=communication_channel)

	def _pack_knx_body(self):
		self.body = bytearray.fromhex(('%02x' % self.communication_channel) + ('%02x' % self.status))
		return self.body


class KnxTunnellingAck(msg.KnxTunnellingAck):

	def __init__(self, request = 0, message=None, communication_channel=None, sequence_count=0):
		self.request = request
		super(KnxTunnellingAck, self).__init__(message=message, communication_channel=communication_channel, sequence_count=sequence_count)


class KnxTunnellingRequestConfirmation(msg.KnxTunnellingRequest):

	def __init__(self, request = 0,  message=None, sockname=None, communication_channel=None,
                 knx_source=None, knx_destination=None, sequence_count=0):
		self.request = request
		super(KnxTunnellingRequestConfirmation, self).__init__(message=message, communication_channel=communication_channel, 
			sequence_count=sequence_count,sockname=sockname, knx_source=knx_source, knx_destination=knx_destination, 
			message_code=0x2e, cemi_ndpu_len=0)

	def _pack_knx_body(self, cemi=None):
		self.body = super(KnxTunnellingRequestConfirmation, self)._pack_knx_body(cemi=cemi) + bytes([0x01,0x00,0x41])
		self.body = self.body[:6] + bytes([0xbc, 0xd0]) + self.body[8:]
		return self.body


class KnxTunnellingRequestIndicator(msg.KnxTunnellingRequest):

	def __init__(self, request = 0,  message=None, sockname=None, communication_channel=None,
                 knx_source=None, knx_destination=None, sequence_count=0):
		self.request = request
		super(KnxTunnellingRequestIndicator, self).__init__(message=message, communication_channel=communication_channel, 
			sequence_count=sequence_count,sockname=sockname, knx_source=knx_source, knx_destination=knx_destination, 
			message_code=0x29, cemi_ndpu_len=0)

	def _pack_knx_body(self, cemi=None):
		self.body = super(KnxTunnellingRequestIndicator, self)._pack_knx_body(cemi=cemi) + bytes([0x01,0x00,0x81])
		self.body = self.body[:6] + bytes([0xbc, 0xc0]) + self.body[8:]
		return self.body