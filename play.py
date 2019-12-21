import mancala
import mcts

def play():
  b = mancala.Board()
  s = b.start()
  ai = mcts.MonteCarlo(b)
  while not b.game_over(s):
    if b.current_player(s) == 1:
      print(s[1:8])
      print(s[8:15])
      p = int(input("Your play {}: ".format(b.legal_plays(s))))
      while not p in b.legal_plays(s):
        p = int(input("Illegal. Pick again: "))
    else:
      p = ai.get_play(s)
      print("Computer plays {}".format(p))
    s = b.next_state(s, p)
  score = b.score(s)
  if score == 1:
    print("You win!")
  if score == -1:
    print("Computer wins!")
  if score == 0:
    print("Tie!")

