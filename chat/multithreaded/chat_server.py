import sys
import socket 
import threading, queue

clients = {}
lock = threading.Lock()


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


def send_msg(sock, msg):
  """ Send a string over a socket, preparing it first """
  msg += '\0'
  data = msg.encode('utf-8')
  sock.sendall(data)


def handle_client_recv(sock, addr):
  """ Receive messages from client and broadcast them to
    other clients until client disconnects """

  rest = bytes()
  while True:
    try:
      (msgs, rest) = recv_msg(sock, rest)
    except (EOFError, ConnectionError):
      handle_disconnect(sock, addr)
      break
    for msg in msgs:
      print('{}: {}'.format(addr, msg))
      
      # Handle first message. Set clients name.
      with lock:
        client_name = clients[sock.fileno()]['name']
        if client_name is None:
          clients[sock.fileno()]['name'] = msg
        else:
          """ Add message to each connected client's send queue """
          msg = '{}: {}'.format(client_name, msg)
          for i in clients:
            clients[i]['queue'].put(msg)

def handle_client_send(sock, q, addr):
  """ Monitor queue for new messages, send them to client as
    they arrive """
  
  while True:
    msg = q.get()
    if msg == None: break
    try:
      send_msg(sock, msg)
    except (ConnectionError, BrokenPipe):
      handle_disconnect(sock, addr)
      break


def handle_disconnect(sock, addr):
  """ Ensure queue is cleaned up and socket closed when a client
    disconnects """

  fd = sock.fileno()
  with lock:
    # Get send queue for this client
    q = clients.get(fd, None)['queue']
    # If we find a queue then this disconnect has not yet
    # been handled
    if q:
      q.put(None)
      del clients[fd]
    
    addr = sock.getpeername()
    print('Client {} disconnected'.format(addr))
    sock.close()


if __name__ == '__main__':
  if len(sys.argv) != 2:
    sys.stderr.write("usage: chat_server port\n")
    exit(1)

  try:
    port = int(sys.argv[1])
    assert port > 0
  except:
    sys.stderr.write("error: invalid port\n")
    exit(1)

  listen_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  listen_sock.bind(("0.0.0.0", port))
  listen_sock.listen(5)
  
  addr = listen_sock.getsockname()
  print('Listening on {}'.format(addr))

  while True:
    client_sock,addr = listen_sock.accept()
    q = queue.Queue()
    with lock:
      clients[client_sock.fileno()] = {
        'name': None,
        'queue': q
      }
    recv_thread = threading.Thread(target=handle_client_recv,
        args=[client_sock, addr], daemon=True)
    send_thread = threading.Thread(target=handle_client_send,
        args=[client_sock, q, addr], daemon=True)
    recv_thread.start()
    send_thread.start()
    print('Connection from {}'.format(addr))
