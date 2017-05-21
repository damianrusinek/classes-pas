import sys
import socket
import ssl
from pprint import pprint

BUF_SIZE = 1024

if __name__ == "__main__":

	if len(sys.argv) != 3:
		sys.stderr.write("usage: tcp_client ip port\n")
		exit(1)

	try:
		addr = sys.argv[1]
		port = int(sys.argv[2])
		assert port > 0 
	except:
		sys.stderr.write("error: invalid port\n")
		exit(1)

	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	ssl_conn = ssl.wrap_socket(sock, cert_reqs=ssl.CERT_REQUIRED, 
		ssl_version=ssl.PROTOCOL_TLSv1_2, ca_certs="trusted_certs.crt")
	print("Connecting...")
	ssl_conn.connect((addr, port))

	# get remote cert
	cert = ssl_conn.getpeercert()
	print("Checking server certificate")
	pprint(cert)
	if not cert or ssl.match_hostname(cert, "PAS - TLS server"):
		raise Exception("Invalid SSL cert.")
	print("Server certificate OK.")

	data = raw_input('Data to send: ')
	ssl_conn.send(data)
	
	print("Response received from server:")
	print(ssl_conn.recv(BUF_SIZE))

	ssl_conn.close()
