import sys
import socket
import getpass

def make_tag(nb):
  return 'CMD' + str(nb).zfill(3)

def parse_resp(resp, tag):
  for line in resp.split('\r\n'):
    if line.startswith(tag):
      if line.split(' ')[1] == 'OK':
        return resp
      else:
        print 'Error:', ' '.join(line.split(' ')[2:]),
        exit(1)
  print 'Error: Malformed response.'
  exit(1)

def parse_search_resp(resp, tag):
  for line in resp.split('\r\n'):
    if line.startswith('* SEARCH'):
      return line.split(' ')[2:]
    elif line.startswith(tag + ' '):
      if line.split(' ')[1] != 'OK':
        print 'Error:', ' '.join(line.split(' ')[2:]),
        exit(1)
  print 'Error: Malformed response.'
  exit(1)

def retrieve_message(sock, tag, msg_id, part):
  msg = '{} FETCH {} ({})\n'.format(tag, msg_id, part)
  sock.send(msg)
  resp = sock.recv(1024)
  while not resp.split('\r\n')[-2].startswith(tag + ' '):
    resp += sock.recv(1024)
  if resp.split('\r\n')[-2].split(' ')[1] != 'OK':
    print 'Error:', ' '.join(resp.split('\r\n')[-1].split(' ')[2:]),
    exit(1)
  if resp.split('\r\n')[-3].startswith('* NO '):
    print 'Error:', resp.split('\r\n')[-2][5:],
    exit(1)
  return '\r\n'.join(resp.split('\r\n')[1:-3])

if __name__ == "__main__":

  if len(sys.argv) != 3:
    sys.stderr.write("usage: %s ip port\n", sys.argv[0])
    exit(1)

  try:
    addr = sys.argv[1]
    port = int(sys.argv[2])
    assert port > 0 
  except:
    sys.stderr.write("error: invalid port\n")
    exit(1)

  username = raw_input('Login:')
  password = getpass.getpass(prompt="Password:")

  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.connect((addr, port))
  
  sock.recv(1024) # Welcome message
  CMDINDEX = 1

  tag = make_tag(CMDINDEX)
  CMDINDEX += 1

  msg = '{} LOGIN {} {}\n'.format(tag, username, password)
  sock.send(msg)
  resp = sock.recv(1024)
  parse_resp(resp, tag)

  tag = make_tag(CMDINDEX)
  CMDINDEX += 1

  msg = '{} SELECT Inbox\n'.format(tag)
  sock.send(msg)
  resp = sock.recv(1024)
  parse_resp(resp,tag)

  tag = make_tag(CMDINDEX)
  CMDINDEX += 1

  msg = '{} SEARCH ALL\n'.format(tag)
  sock.send(msg)
  resp = sock.recv(1024)
  messages_ids = parse_search_resp(resp, tag)

  for msg_id in messages_ids:
    tag = make_tag(CMDINDEX)
    CMDINDEX += 1
    print 'Message id:', msg_id
    print 'Message body:'
    print retrieve_message(sock, tag, msg_id, 'BODY[TEXT]')
    tag = make_tag(CMDINDEX)
    CMDINDEX += 1
    print 'Whole message:'
    print retrieve_message(sock, tag, msg_id, 'RFC822')
    print '---------------'


  tag = make_tag(CMDINDEX)
  CMDINDEX += 1
  msg = '{} CLOSE\n'.format(tag)
  sock.send(msg)
  sock.recv(1024)

  tag = make_tag(CMDINDEX)
  CMDINDEX += 1
  msg = '{} LOGOUT\n'.format(tag)
  sock.send(msg)
  sock.recv(1024)

  sock.close()
