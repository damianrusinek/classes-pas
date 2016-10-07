import sys
import socket

BUF_SIZE = 1024

if __name__ == "__main__":

  if len(sys.argv) != 2:
    sys.stderr.write("usage: udp_server port\n")
    exit(1)

  try:
    port = int(sys.argv[1])
    assert port > 0 
  except:
    sys.stderr.write("error: invalid port\n")
    exit(1)

  sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  sock.bind(("0.0.0.0", port))

  while True:
    data, addr = sock.recvfrom(BUF_SIZE)
    print(addr[0], "sent a message.")  

    sock.sendto(data, addr)

  sock.close()
