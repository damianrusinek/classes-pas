import sys
import socket

BUF_SIZE = 1024

if __name__ == "__main__":

  if len(sys.argv) != 2:
    sys.stderr.write("usage: chat_server port\n")
    exit(1)

  try:
    port = int(sys.argv[1])
    assert port > 0 
  except:
    sys.stderr.write("error: invalid port\n")
    exit(1)

  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.bind(("0.0.0.0", port))
  sock.listen(5)

  while True:
    client, addr = sock.accept()
    print(addr[0], "connected now.")  
    print 'Receive and send messages. Empty line closes connection.'

    while True:
        data = client.recv(BUF_SIZE)
        if not data:
          break
        print 'Msg:', data

        data = raw_input('Answer:')
        if data == '':
          break
        client.send(data)

    client.close()

  sock.close()
