import sys
import socket

if __name__ == '__main__':

  if len(sys.argv) != 2:
    sys.stderr.write("usage: dns_client address\n")
    exit(1)

  hostname = sys.argv[1]
  ip_address = socket.gethostbyname(hostname)
  print("IP address: {0}".format(ip_address))
