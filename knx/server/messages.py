import sys, struct
from os import path

sys.path.append(path.join(path.sep, 'opt', 'knxmap'))
from libknxmap import messages as msg


class KnxDescriptionResponse(msg.KnxDescriptionResponse):

	def __init__(self, message=None, request=None):
		self.request = request
		super(KnxDescriptionResponse, self).__init__(message=message)

	def _pack_knx_body(self):
		self.body = bytearray.fromhex('3601020000000000b8874bdf6e7fe000170c0242ac1100026b6e7864000000000000000'+
		'00000000000000000000000000000000000000a020201030104010501')
		return self.body


class KnxConnectResponse(msg.KnxConnectResponse):

	def __init__(self, message=None, request=None, communication_channel=None, status=0):
		self.request = request
		self.status = status
		self.communication_channel = communication_channel
		super(KnxConnectResponse, self).__init__(message=message)

	def _pack_knx_body(self):
		self.body = bytearray.fromhex(('%02x' % self.communication_channel) + ('%02x' % self.status) + '080100000000000004040000')
		return self.body


class KnxDisconnectResponse(msg.KnxDisconnectResponse):

	def __init__(self, message=None, request=None, communication_channel=1, status=0):
		self.request = request
		self.status = status
		super(KnxDisconnectResponse, self).__init__(message=message, communication_channel=communication_channel)

	def _pack_knx_body(self):
		self.body = bytearray.fromhex(('%02x' % self.communication_channel) + ('%02x' % self.status))
		return self.body


class KnxConnectionStateResponse(msg.KnxConnectionStateResponse):

	def __init__(self, message=None, request=None, communication_channel=1, status=0):
		self.request = request
		self.status = status
		super(KnxConnectionStateResponse, self).__init__(message=message, communication_channel=communication_channel)

	def _pack_knx_body(self):
		self.body = bytearray.fromhex(('%02x' % self.communication_channel) + ('%02x' % self.status))
		return self.body