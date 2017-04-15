import sys
import json
import urllib2

def get(url):
  req = urllib2.Request(url=url)
  return urllib2.urlopen(req)

if __name__ == '__main__':

  if len(sys.argv) != 2:
    sys.stderr.write("usage: %s username\n" % sys.argv[0])
    exit(1)

  APIURL = 'https://api.github.com'

  username = sys.argv[1]

  # Get basic info
  url = APIURL + '/users/' + username
  r = get(url)
  basicinfo = json.loads(r.read())

  # Download avatar
  if basicinfo['avatar_url']:
    print 'Downloading avatar...'
    r = get(basicinfo['avatar_url'])
    with open(username+'.jpg', 'wb') as f:
      f.write(r.read())
    print 'Downloaded'
    
  # Get gists
  print 'Downloading gists...'
  url = APIURL + '/users/' + username + '/gists'
  r = get(url)
  gists = json.loads(r.read())
  print '  Found %d gists' % len(gists)

  for g in gists:
    gid = g['id']
    print "  Downloading gist %s" % gid
    for f in g['files']:
      print "    Downloading file %s" % f
      url = g['files'][f]['raw_url']
      r = get(url)
      with open(gid + '_' + f, 'wb') as ff:
        ff.write(r.read())
      print "    Downloaded"
    print "  Downloaded"



