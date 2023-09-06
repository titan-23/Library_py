from array import array

class BitVector():

  # 簡潔ではない
  # コンパクトのつもり

  def __init__(self, n: int):
    assert 0 <= n < 4294967295
    self.N = n
    self.block_size = (n + 31) >> 5
    # bit数 32*n/32 * 2 = 2n bit
    b = bytes(4*(self.block_size+1))
    self.bit = array('I', b)
    self.acc = array('I', b)

  @staticmethod
  def _popcount(x: int) -> int:
    x = x - ((x >> 1) & 0x55555555)
    x = (x & 0x33333333) + ((x >> 2) & 0x33333333)
    x = x + (x >> 4) & 0x0f0f0f0f
    x += x >> 8
    x += x >> 16
    return x & 0x0000007f

  def set(self, k: int) -> None:
    self.bit[k>>5] |= 1 << (k & 31)

  def build(self) -> None:
    acc, bit = self.acc, self.bit
    for i in range(self.block_size):
      acc[i+1] = acc[i] + BitVector._popcount(bit[i])

  def access(self, k: int) -> int:
    return (self.bit[k >> 5] >> (k & 31)) & 1

  def __getitem__(self, k: int) -> int:
    return (self.bit[k >> 5] >> (k & 31)) & 1

  def rank0(self, r: int) -> int:
    # a[0, r) に含まれる 0 の個数
    return r - (self.acc[r>>5] + BitVector._popcount(self.bit[r>>5] & ((1 << (r & 31)) - 1)))

  def rank1(self, r: int) -> int:
    # a[0, r) に含まれる 1 の個数
    return self.acc[r>>5] + BitVector._popcount(self.bit[r>>5] & ((1 << (r & 31)) - 1))

  def rank(self, r: int, v: int) -> int:
    # a[0, r) に含まれる v の個数
    return self.rank1(r) if v else self.rank0(r)

  def select0(self, k: int) -> int:
    # k 番目の 0 のindex
    # O(log(N))
    if k < 0 or self.rank0(self.N) <= k:
      return -1
    l, r = 0, self.block_size+1
    while r - l > 1:
      m = (l + r) >> 1
      if m*32 - self.acc[m] > k:
        r = m
      else:
        l = m
    indx = 32 * l
    k = k - (l*32 - self.acc[l]) + self.rank0(indx)
    l, r = indx, indx+32
    while r - l > 1:
      m = (l + r) >> 1
      if self.rank0(m) > k:
        r = m
      else:
        l = m
    return l

  def select1(self, k: int) -> int:
    # k 番目の 1 のindex
    # O(log(N))
    if k < 0 or self.rank1(self.N) <= k:
      return -1
    l, r = 0, self.block_size+1
    while r - l > 1:
      m = (l + r) >> 1
      if self.acc[m] > k:
        r = m
      else:
        l = m
    indx = 32 * l
    k = k - self.acc[l] + self.rank1(indx)
    l, r = indx, indx+32
    while r - l > 1:
      m = (l + r) >> 1
      if self.rank1(m) > k:
        r = m
      else:
        l = m
    return l

  def select(self, k: int, v: int) -> int:
    # k 番目の v のindex
    # O(log(N))
    return self.select1(k) if v else self.select0(k)

