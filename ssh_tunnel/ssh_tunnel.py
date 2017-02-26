import sys
from sshtunnel import SSHTunnelForwarder  
from getpass import getpass


if __name__ == "__main__":

  if len(sys.argv) != 3:
    sys.stderr.write("usage: %s user@ssh_server:ssh_port destination_server:destination_port\n" % \
      sys.argv[0])
    exit(1)

  try:
    ssh_port = sys.argv[1].split(':')[1]
    ssh_port = int(ssh_port)
    assert ssh_port > 0 
  except:
    sys.stderr.write("error: invalid ssh port\n")
    exit(1)

  try:
    ssh_user = sys.argv[1].split('@')[0]
    ssh_addr = sys.argv[1].split('@')[1].split(':')[0]
  except:
    sys.stderr.write("error: invalid ssh address\n")
    exit(1)

  try:
    destination_port = sys.argv[2].split(':')[1]
    destination_port = int(destination_port)
    assert destination_port > 0 
    destination_addr = sys.argv[2].split(':')[0]
  except:
    sys.stderr.write("error: invalid destination port\n")
    exit(1)

  ssh_password = getpass('Enter password for %s@%s:%s : ' % (ssh_user, ssh_addr, ssh_port))
  server = SSHTunnelForwarder(ssh_address=(ssh_addr, ssh_port), ssh_username=ssh_user,
    ssh_password=ssh_password, remote_bind_address=(destination_addr, destination_port))
  server.start()
  
  print('Connected the remote service via local port: %s' %server.local_bind_port)
  try:
    while True:
      pass
  except KeyboardInterrupt:
    print("Exiting user user request.\n")
  server.stop()