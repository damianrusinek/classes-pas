import sys
import socket

BUF_SIZE = 1024

def get_resp_code(line):
  return int(line[:3])

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

  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  try:  
    sender_email = raw_input('Sender e-mail:')
    
    print 'Please provide receivers\' e-mails in separate lines (emty line ends list):'
    receiver_emails = []
    receiver_email = raw_input('')
    while receiver_email != '':
      receiver_emails.append(receiver_email)
      receiver_email = raw_input('')

    subject = raw_input('Subject:')

    msg = ''
    msg += 'From: %s\r\n' % (sender_email,)
    for receiver_email in receiver_emails:
      msg += 'To: %s\r\n' % (receiver_email,)
    msg += 'Subject: %s\r\n' % (subject,)
    msg += '\r\n'
    
    print 'Please provide message (empty line ends message):'
    msg_line = raw_input('')
    while msg_line != '':
      msg += msg_line + '\r\n'
      msg_line = raw_input('')
    msg += '.\r\n'

    sock.connect((addr, port))
    data = sock.recv(BUF_SIZE)
    code = get_resp_code(data)
    if code != 220:
      print 'Cannot connect to server.'
      exit(1)

    sock.send('HELO example.com\r\n')
    data = sock.recv(BUF_SIZE)
    code = get_resp_code(data)
    if code != 250:
      print 'Error on HELO command:', data[4:]
      exit(1)

    sock.send('MAIL FROM: %s\r\n' % (sender_email,))
    data = sock.recv(BUF_SIZE)
    code = get_resp_code(data)
    if code != 250:
      print 'Error on MAIL FROM command:', data[4:]
      exit(1)

    for receiver_email in receiver_emails:
      sock.send('RCPT TO: %s\n' % (sender_email,))
      data = sock.recv(BUF_SIZE)
      code = get_resp_code(data)
      if code != 250:
        print 'Error on RCPT TO command:', data[4:]
        exit(1)

    sock.send('DATA\r\n')
    data = sock.recv(BUF_SIZE)
    code = get_resp_code(data)
    if code != 354:
      print 'Error on DATA command:', data[4:]
      exit(1)

    sock.send(msg)
    data = sock.recv(BUF_SIZE)
    code = get_resp_code(data)
    if code != 250:
      print 'Error on message:', data[4:]
      exit(1)

    sock.send('QUIT\r\n')
    data = sock.recv(BUF_SIZE)
    code = get_resp_code(data)
    if code != 221:
      print 'Error on QUIT command:', data[4:]
      exit(1)

    print 'E-mail sent.'
    sock.close()

  except socket.error, e:
    print 'Error:', e