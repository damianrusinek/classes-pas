import sys
import socket

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
  try:
    sock.connect((addr, port))
  
    while True:
      data = raw_input('Data to send (empty line quits):')
      if data == '':
        break
      sock.send(data)
      data = sock.recv(BUF_SIZE)
      if not data:
        break
      print 'Answer:', data
    sock.close()

  except socket.error, e:
    print 'Error:', e
