class Board(object):
  def start(self):
    # state[0] is which player it is (1 or 2)
    # state[7] is player 1's store
    # state[14] is player 2's store
    return (1,4,4,4,4,4,4,0,4,4,4,4,4,4,0)

  def current_player(self, state):
    return state[0]

  def next_state(self, state, play):
    player = self.current_player(state)
    next_player = 3 - player
    idx = 7*(player-1) + play
    idxs_to_skip = [0, 7*(next_player)]
    state = list(state)
    count = state[idx]
    state[idx] = 0
    while count > 0:
      idx = (idx + 1) % 15
      if idx in idxs_to_skip:
        continue
      state[idx] += 1
      count -= 1
    if idx != 7*player:
      state[0] = next_player
    return tuple(state)

  def legal_plays(self, state):
    player = self.current_player(state)
    def legal(play):
      idx = 7*(player-1) + play
      return state[idx] > 0
    return filter(legal, range(1,7))

  def winner(self, state):
    if len(self.legal_plays(state)) > 0:
      return 0
    def score(player):
      return sum(state[7*(player-1) + 1:7*player + 1])
    s1 = score(1)
    s2 = score(2)
    if s1 > s2:
      return 1
    if s1 < s2:
      return 2
    if s1 == s2:
      return -1
