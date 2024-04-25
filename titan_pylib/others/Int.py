import random

class Int(int):

  _rand = random.getrandbits(32)
  while _rand == 0:
    random.getrandbits(32)

  def __init__(self, x: int):
      int.__init__(x)

  def __hash__(self):
      return super(Int, self).__hash__() ^ Int._rand

