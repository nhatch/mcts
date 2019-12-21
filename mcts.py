# Monte Carlo Tree Search
# Modified from https://jeffbradberry.com/posts/2015/09/intro-to-monte-carlo-tree-search/

import datetime
import math
import random

class MonteCarlo(object):
  def __init__(self, board):
    self.board = board
    self.calculation_time = datetime.timedelta(seconds=2)
    self.max_plays = 150 # Mancala games are usually less than 150 moves long
    self.exploration_constant = 1.4
    # Stores total scores for each expanded state (accumulated over the course of the game)
    self.score = {}
    self.plays = {}

  def get_play(self, state):
    self.max_depth = 0
    begin = datetime.datetime.utcnow()
    games = 0
    while datetime.datetime.utcnow() - begin < self.calculation_time:
      self.run_simulation(state)
      games += 1
    print(games, datetime.datetime.utcnow() - begin)
    legal = self.board.legal_plays(state)
    plays_states = [(p, self.board.next_state(state, p)) for p in legal]
    stats = sorted([
        (
          self.value(self.board.current_player(state), S),
          self.score.get(S, 0),
          self.plays.get(S, 0),
          p
        ) for p, S in plays_states
    ], reverse=True)
    for x in stats:
      print("{3}: {0:.4f} ({1:.1f} / {2})".format(*x))
    print("Maximum depth searched:", self.max_depth)
    return stats[0][3]

  def value(self, player, state):
    avg = self.score.get(state, 0) / self.plays.get(state, 1)
    return avg * (1 if player == 1 else -1)

  def run_simulation(self, state):
    visited_states = set()
    expand = True
    for t in range(1, self.max_plays + 1):
      legal = self.board.legal_plays(state)
      plays_states = [(p, self.board.next_state(state, p)) for p in legal]
      if all(S in self.plays for _, S in plays_states):
        log_total = math.log(sum(self.plays[S] for _, S in plays_states))
        bounds_plays = [
            # UCB1 (upper confidence bound)
            (self.value(self.board.current_player(state), S) + math.sqrt(self.exploration_constant * log_total / self.plays[S]), p, S)
            for p, S in plays_states
        ]
        _, play, state = max(bounds_plays)
      else:
        play, state = random.choice(plays_states)
      visited_states.add(state)
      if expand and not state in self.plays:
        expand = False
        self.plays[state] = 0
        self.score[state] = 0.0
        if t > self.max_depth:
          self.max_depth = t
      if self.board.game_over(state):
        break
    for S in visited_states:
      if S in self.plays:
        self.plays[S] += 1
        self.score[S] += self.board.score(state)

