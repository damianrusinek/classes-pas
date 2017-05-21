import sys
import socket
import threading
import ssl


def send_msg(sock, msg):
	""" Send a string over a socket, preparing it first """
	msg += '\0'
	data = msg.encode('utf-8')
	sock.sendall(data)


def parse_recvd_data(data):
  """ Break up raw received data into messages, delimited
    by null byte """
  parts = data.split(b'\0')
  msgs = parts[:-1]
  rest = parts[-1]
  return (msgs, rest)
  

def recv_msg(sock, data=bytes()):
	""" Receive data and break into complete messages on null byte
		delimiter. Block until at least one message received, then
		return received messages """
	
	msgs = []
	while not msgs:
		recvd = sock.recv(4096)
		if not recvd:
			raise ConnectionError()
		data = data + recvd
		(msgs, rest) = parse_recvd_data(data)
	msgs = [msg.decode('utf-8') for msg in msgs]
	return (msgs, rest)


def handle_input(ssl_sock, sock):
	""" Prompt user for message and send it to server """
	print("Type messages, enter to send. 'q' to quit")
	while True:
		msg = input() # Blocks
		if msg == 'q':
			ssl_sock.close()
			sock.shutdown(socket.SHUT_RDWR)
			sock.close()
			break
		try:
			send_msg(ssl_sock, msg) # Blocks until sent
		except (BrokenPipeError, ConnectionError):
			break

if __name__ == "__main__":

	if len(sys.argv) != 3:
		sys.stderr.write("usage: chat_client ip port\n")
		exit(1)

	try:
		addr = sys.argv[1]
		port = int(sys.argv[2])
		assert port > 0 
	except:
		sys.stderr.write("error: invalid port\n")
		exit(1)

	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	ssl_sock = ssl.wrap_socket(sock, cert_reqs=ssl.CERT_REQUIRED, 
		ssl_version=ssl.PROTOCOL_TLSv1_2, ca_certs="trusted_certs.crt")
	ssl_sock.connect((addr, port))
	print('Connected to {}:{}'.format(addr, port))

	# check remote cert
	cert = ssl_conn.getpeercert()
	print("Checking server certificate")
	if not cert or ssl.match_hostname(cert, "PAS - TLS server"):
		raise Exception("Invalid SSL cert.")
	print("Server certificate OK.")

	# Create thread for handling user input and message sending
	thread = threading.Thread(target=handle_input, args=[ssl_sock, sock], daemon=True)
	thread.start()
	
	rest = bytes()
	addr = ssl_sock.getsockname()
	# Loop indefinitely to receive messages from server
	while True:
		try:
			# blocks
			(msgs, rest) = recv_msg(ssl_sock, rest)
			for msg in msgs:
				print(msg)
		except ConnectionError:
			print('Connection to server closed')
			sock.close()
			break
