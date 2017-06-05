import sys
import socket 
import select
from types import SimpleNamespace
from collections import deque

clients = {}


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


def create_client(sock):
  """ Return an object representing a client """
  return SimpleNamespace(sock=sock, rest=bytes(), 
                         send_queue=deque(), name=None)


def prep_msg(msg):
  """ Prepare message """
  msg += '\0'
  return msg.encode('utf-8')


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
  poll = select.poll()
  poll.register(listen_sock, select.POLLIN)
  
  addr = listen_sock.getsockname()
  print('Listening on {}'.format(addr))

  while True:

    # Iterate over all sockets with events
    for fd, event in poll.poll():
      # clear-up a closed socket
      if event & (select.POLLHUP | select.POLLERR | select.POLLNVAL):
        poll.unregister(fd)
        del clients[fd]

      # Accept new connection, add client to clients dict
      elif fd == listen_sock.fileno():
        client_sock,addr = listen_sock.accept()
        client_sock.setblocking(False)
        fd = client_sock.fileno()
        clients[fd] = create_client(client_sock)
        poll.register(fd, select.POLLIN)
        print('Connection from {}'.format(addr))

      # Handle received data on socket
      elif event & select.POLLIN:
        client = clients[fd]
        addr = client.sock.getpeername()
        try:
          msgs, client.rest = recv_msg(client.sock, client.rest)
        except ConnectionError:
          # the client state will get cleaned up in the
          # next iteration of the event loop, as close()
          # sets the socket to POLLNVAL
          client.sock.close()
          print('Client {} disconnected'.format(addr))
          continue
        # If we have any messages, broadcast them to all
        # clients
        for msg in msgs:
          print('{}: {}'.format(addr, msg))
          
          # Handle first message. Set clients name.
          if client.name is None:
            client.name = msg
          else:
            """ Add message to each connected client's send queue """
            msg = '{}: {}'.format(client.name, msg)
            for i in clients:
              clients[i].send_queue.append(prep_msg(msg))
              poll.register(clients[i].sock, select.POLLOUT)

      # Send message to ready client
      elif event & select.POLLOUT:
        client = clients[fd]
        data = client.send_queue.popleft()
        sent = client.sock.send(data)
        if sent < len(data):
          client.rest.appendleft(data[sent:])
        if not client.send_queue:
          poll.modify(client.sock, select.POLLIN)
