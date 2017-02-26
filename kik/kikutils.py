
MSG_SIZE = 10

def pad_msg(msg):
  return msg + ' ' * (MSG_SIZE - len(msg))

def print_board(board, numbers=False):
  print '%s|%s|%s' % (
    board[0] if board[0] != '?' else '0' if numbers else ' ', 
    board[1] if board[1] != '?' else '1' if numbers else ' ', 
    board[2] if board[2] != '?' else '2' if numbers else ' ')
  print '-----'
  print '%s|%s|%s' % (
    board[3] if board[3] != '?' else '3' if numbers else ' ', 
    board[4] if board[4] != '?' else '4' if numbers else ' ', 
    board[5] if board[5] != '?' else '5' if numbers else ' ')
  print '-----'
  print '%s|%s|%s' % (
    board[6] if board[6] != '?' else '6' if numbers else ' ', 
    board[7] if board[7] != '?' else '7' if numbers else ' ', 
    board[8] if board[8] != '?' else '8' if numbers else ' ')

def check_winner(board):
  if board[0] == board[1] == board[2] and board[0] != '?':
    return board[0]
  if board[3] == board[4] == board[5] and board[3] != '?':
    return board[3]
  if board[6] == board[7] == board[8] and board[6] != '?':
    return board[6]
  if board[0] == board[4] == board[8] and board[0] != '?':
    return board[0]
  if board[2] == board[4] == board[7] and board[2] != '?':
    return board[2]
  if board[0] == board[3] == board[7] and board[0] != '?':
    return board[0]
  if board[1] == board[4] == board[7] and board[1] != '?':
    return board[1]
  if board[2] == board[5] == board[8] and board[2] != '?':
    return board[2]
  return None


