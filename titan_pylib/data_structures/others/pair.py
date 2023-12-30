class Pair():

  # pair<unsigned int, unsigned int>

  def __init__(self, first: int, second: int):
    self.d = (first << 32) | second

  def __getitem__(self, k: int):
    return self.d >> 32 if k == 0 else self.d & 4294967295

  def __setitem__(self, k: int, v: int):
    self.d = (v << 32) | (self.d & 4294967295) if k == 0 else self.d >> 32 << 32 | v

  @property
  def first(self) -> int:
    return self.d >> 32

  @property
  def second(self) -> int:
    return self.d & 4294967295

  @first.setter
  def first(self, v: int):
    self.d = (v << 32) | (self.d & 4294967295)

  @second.setter
  def second(self, v: int):
    self.d = self.d >> 32 << 32 | v

  def __hash__(self):
    return self.d

  def __str__(self):
    return f'[{self.d >> 32}, {self.d & 4294967295}]'

  def __repr__(self):
    return f'Pair({self.first}, {self.second})'

