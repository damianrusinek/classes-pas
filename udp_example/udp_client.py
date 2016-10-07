import sys
import socket

BUF_SIZE = 1024

if __name__ == "__main__":

  if len(sys.argv) != 3:
    sys.stderr.write("usage: udp_client ip port\n")
    exit(1)

  try:
    addr = sys.argv[1]
    port = int(sys.argv[2])
    assert port > 0 
  except:
    sys.stderr.write("error: invalid port\n")
    exit(1)

  sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  try:  
    while True:
      data = raw_input('Data to send (empty line quits):')
      if data == '':
        break
      sock.sendto(data, (addr, port))
      data, recv_addr = sock.recvfrom(BUF_SIZE)
      print 'Answer:', data
    sock.close()

  except socket.error, e:
    print 'Error:', e
