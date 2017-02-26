import sys
import socket
from kikutils import *

MY_SIGN = 'o'
THEIR_SIGN = 'x'

if __name__ == "__main__":

  if len(sys.argv) != 2:
    sys.stderr.write("usage: %s port\n" % (sys.argv[0], ))
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
    board = '?' * 9

    cmd = client.recv(MSG_SIZE).strip()
    if cmd != 'START':
      print 'Invalid command'
      client.send(pad_msg('ERROR'))
      client.close()
      continue

    client.send(pad_msg('OK'))

    while True:
      cmd = client.recv(MSG_SIZE).strip()

      if cmd == 'END' or cmd == '':
        print_board(board)
        winner = check_winner(board)
        if winner is None:
          print 'Game ended unexpectedly.'
        if winner == MY_SIGN:
          print 'You won!'
        else:
          print 'You lost!'
        client.close()
        break

      if cmd.startswith('CHECK '):
        try:
          fieldnb =  int(cmd.split(' ')[1])
          if fieldnb < 0 or fieldnb > 8:
            raise ValueError
        except ValueError:
          print 'Invalid command'
          client.send(pad_msg('ERROR'))
          client.close()
          break

        if board[fieldnb] != '?':
          print 'Field taken'
          client.send(pad_msg('ERROR'))
          client.close()
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

        client.send(pad_msg('OK'))  

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
            continue

        board[fieldnb] = MY_SIGN
        client.send(pad_msg('CHECK ' + str(fieldnb)))    
        
        if client.recv(MSG_SIZE).strip() != 'OK':
          print 'Invalid repsonse:', resp
          client.close()
          break

      print 'Invalid command'
      client.send(pad_msg('ERROR'))
      client.close()
      break
