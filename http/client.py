import sys
import socket
import urlparse

CRLF = "\r\n"

def recvuntil(s, needle):
  data = ""
  while data[-len(needle):] != needle:
    data += s.recv(1)
  return data

def recvall(s, n):
  data = ""
  while len(data) < n:
    data += s.recv(1)
  return data

def parse_headers(headers_string):
  firstline_elems = [  
    s.strip() for s in headers_string.split(CRLF)[0].split(' ') 
  ]
  protocol, status, status_name = firstline_elems[0], firstline_elems[1], ' '.join(firstline_elems[2:])
  status = int(status)
  headers = dict([(s.split(':')[0].lower(), ':'.join(s.split(':')[1:])) 
    for s in headers_string.strip().split(CRLF)[1:]])
  return status, headers

def get(url):

  url = urlparse.urlparse(url)
  path = url.path
  if path == "":
      path = "/"
  HOST = url.netloc if url.port is None else ':'.join(url.netloc.split(':')[:-1])
  PORT = 80 if url.port is None else int(url.port)

  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  s.connect((HOST, PORT))
  s.settimeout(0.3)

  request = "" + \
    "GET %s HTTP/1.1%s" % (path, CRLF) + \
    "Host: %s%s" % (HOST, CRLF) + \
    CRLF

  s.send(request)
  resp_headers = recvuntil(s, CRLF + CRLF)
  
  status, headers = parse_headers(resp_headers)

  redirected_to = None
  if 300 <= status < 400:
    if 'location' in headers:
      redirected_to = headers['location']

  if redirected_to is None:
    if 'content-length' in headers:
      size = int(headers['content-length'])
      data = recvall(s, size)
    else:
      data = ""
    s.shutdown(1)
    s.close()
    return status, data

  s.shutdown(1)
  s.close()
  return get(redirected_to)

def get_filename(url):
  url = urlparse.urlparse(url)
  path = url.path
  if path == "":
      return 'index.html'
  return path.split('/')[-1]
   
if __name__ == "__main__":

  if len(sys.argv) != 2:
    sys.stderr.write("usage: %s url\n" % sys.argv[0])
    exit(1)

  url = sys.argv[1]

  status, data = get(url)

  print 'Server returned status', status
  if len(data) > 0:
    filename = get_filename(url)
    with open(filename, 'wb') as f:
      f.write(data)
    print 'Data saved to file', filename

  
  