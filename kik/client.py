import sys
import socket
from kikutils import *

MY_SIGN = 'x'
THEIR_SIGN = 'o'

if __name__ == "__main__":

  if len(sys.argv) != 3:
    sys.stderr.write("usage: %s ip port\n" % (sys.argv[0], ))
    exit(1)

  try:
    addr = sys.argv[1]
    port = int(sys.argv[2])
    assert port > 0 
  except:
    sys.stderr.write("error: invalid port\n")
    exit(1)

  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.connect((addr, port))

  board = '?' * 9
  sock.send(pad_msg('START'))
  resp = sock.recv(MSG_SIZE).strip()
  if resp != 'OK':
    print 'Invalid response:', resp
    sock.close()
    exit(1)

  while True:
    # Select field
    while True:
      print_board(board, numbers=True)
      try:
        fieldnb = int(raw_input('What is your field number? '))
        if fieldnb < 0 or fieldnb > 8:
          raise ValueError
        if board[fieldnb] != '?':
          print 'This field is not empty'
        else:
          break
      except ValueError:
        print 'Invalid field number'

    board[fieldnb] = MY_SIGN
    sock.send(pad_msg('CHECK ' + str(fieldnb)))
    if sock.recv(MSG_SIZE).strip() != 'OK':
      print 'Invalid repsonse:', resp
      sock.close()
      break

    cmd = sock.recv(MSG_SIZE).strip()

    if cmd == 'END' or cmd == '':
      print_board(board)
      winner = check_winner(board)
      if winner is None:
        print 'Game ended unexpectedly.'
      if winner == MY_SIGN:
        print 'You won!'
      else:
        print 'You lost!'
      sock.close()
      break

    if cmd.startswith('CHECK '):
      try:
        fieldnb =  int(cmd.split(' ')[1])
        if fieldnb < 0 or fieldnb > 8:
          raise ValueError
      except ValueError:
        print 'Invalid command'
        sock.send(pad_msg('ERROR'))
        sock.close()
        break

      if board[fieldnb] != '?':
        print 'Field taken'
        sock.send(pad_msg('ERROR'))
        sock.close()
        break

      board[fieldnb] = THEIR_SIGN
      winner = check_winner(board)
      if winner in [MY_SIGN, THEIR_SIGN]:
        print_board(board)
        if winner == MY_SIGN:
          print 'You won!'
        else:
          print 'You lost!'
        client.send(pad_msg('END'))
        client.close()
        break

    print 'Invalid command'
    client.send(pad_msg('ERROR'))
    client.close()
    break
