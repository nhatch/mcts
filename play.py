import mancala
import random

def play():
  b = mancala.Board()
  s = b.start()
  while b.winner(s) == 0:
    if b.current_player(s) == 1:
      print s[1:8]
      print s[8:15]
      p = int(input("Your play {}: ".format(b.legal_plays(s))))
      while not p in b.legal_plays(s):
        p = int(input("Illegal. Pick again: "))
    else:
      p = random.choice(b.legal_plays(s))
      print "Computer plays {}".format(p)
    s = b.next_state(s, p)
  winner = b.winner(s)
  if winner == 1:
    print "You win!"
  if winner == 2:
    print "Computer wins!"
  if winner == -1:
    print "Tie!"

