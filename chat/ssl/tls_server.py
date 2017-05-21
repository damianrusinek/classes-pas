import sys
import ssl
import socket

BUF_SIZE = 1024

if __name__ == "__main__":

	if len(sys.argv) != 2:
		sys.stderr.write("usage: tcp_server port\n")
		exit(1)

	try:
		port = int(sys.argv[1])
		assert port > 0 
	except:
		sys.stderr.write("error: invalid port\n")
		exit(1)

	server_socket = socket.socket()
	server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	server_socket.bind(("0.0.0.0", port))
	server_socket.listen(5)
	print("Waiting for ssl client on port %s" % port)

	try:
		while True:
			try:
				client, addr = server_socket.accept()
				print("Client connected")
				# Generate your server's public certificate and private key			
				ssl_client = ssl.wrap_socket(client, server_side=True, 
					certfile="server.crt", keyfile="server.key", 
					ssl_version=ssl.PROTOCOL_TLSv1_2)
				print("TLS connection intiated")

				data = ssl_client.recv(BUF_SIZE)
				print("Received: %s" % data)
				
				ssl_client.send(data)
				ssl_client.close()
				client.close()
			except ssl.SSLError:
				pass				
	except KeyboardInterrupt:
		server_socket.close()
		print("Finished.")