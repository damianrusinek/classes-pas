import imaplib
import getpass

IMAP_SERVER_ADDR = '127.0.0.1'
IMAP_SERVER_PORT = 143

def show_emails(server, port, username, password):
  mailbox = imaplib.IMAP4(server, port)
  resp, msg = mailbox.login(username, password)
  if resp != 'OK':
    print 'Auth error: %s' % msg[0]
    exit(1)
  resp, msg = mailbox.select('Inbox')
  if resp != 'OK':
    print 'Select mailbox error: %s' % msg[0]
    exit(1)

  resp, data = mailbox.search(None, 'ALL')
  
  for num in data[0].split():
    resp, msg = mailbox.fetch(num, '(RFC822)')
    resp, text = mailbox.fetch(num, '(BODY[TEXT])')
    print 'Message no.  %s\n' % (num,)
    print 'Message body:'
    print text[0][1]
    print 'Whole message:'
    print msg[0][1]
    print '---------------'

  mailbox.close()
  mailbox.logout()

if __name__ == '__main__':
  username = raw_input("Login: ")
  password = getpass.getpass(prompt="Password:")
  
  show_emails(IMAP_SERVER_ADDR, IMAP_SERVER_PORT, username, password)