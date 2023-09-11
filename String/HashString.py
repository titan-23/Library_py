import random

# HashString_MOD = 2**61-1  # MODはglobalにとる
HashString_MOD = 998244353
class HashString:

  def __init__(self, s: str):
    self.b = random.randint(37, 10000)
    self.n = len(s)
    self.data = [0] * (self.n+1)
    self.powb = [1] * (self.n+1)
    for i in range(1, self.n+1):
      self.powb[i] = self.powb[i-1] * self.b % HashString_MOD
      self.data[i] = (self.b * self.data[i-1] + ord(s[i-1])) % HashString_MOD

  def get(self, l: int, r: int) -> int:
    return (self.data[r] - self.data[l] * self.powb[r-l]) % HashString_MOD

  def __getitem__(self, item) -> int:
    if isinstance(item, int):
      return (self.data[item+1] - self.data[item] * self.powb[1]) % HashString_MOD
    else:
      start = item.start
      stop = item.stop
      if start is None:
        start = 0
      if stop is None:
        stop = self.n
      return self.get(start, stop)

  def update(self, h: int, c1: str, c2: str, k: int) -> int:
    '''
    h1: int  元のハッシュ
    c1: char 元の文字
    c2: char 新たな文字
    k : int  変える桁 ZeroIndexed
    '''
    return (h + (ord(c2) - ord(c1))*self.powb[self.n-k-1]) % HashString_MOD

  def unite(self, h1: int, h2: int, k: int) -> int:
    return (h1 * self.powb[k] + h2) % HashString_MOD

  def popleftappend(self, h: int, c1: str, c2: str) -> int:
    '''
    hの長さはnであると仮定
    c1は元の文字, c2は新たな文字
    '''
    return ((h - ord(c1)*self.powb[self.n-1]) * self.b + ord(c2)) % HashString_MOD

