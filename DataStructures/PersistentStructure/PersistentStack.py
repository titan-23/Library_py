from typing import Any

class PersistentStack():

  class NilNode:

    def top(self) -> None:
      return None

    def append(self, x: Any) -> 'PersistentStack':
      return PersistentStack(x)

    def pop(self) -> None:
      assert False, 'pop() from empty PersistentStack'

    def __str__(self):
      return '[]'

    def __len__(self):
      return 0

    def __bool__(self):
      return False

  NIL = NilNode()

  def __init__(self, val: Any=None, prev=NIL):
    self.val = val
    self.prev = prev
    self.len = len(prev) + (val is not None)

  def top(self) -> Any:
    return self.val

  def append(self, x: Any):
    return PersistentStack(x, self)

  def pop(self):
    return self.prev

  def __bool__(self):
    return self.val is not None

  def __len__(self):
    return self.len

  def __str__(self):
    res, now, NIL = [], self, PersistentStack.NIL
    while now is not NIL:
      res.append(now.val)
      now = now.pop()
    res.pop()
    return '[' + ', '.join(map(str, res[::-1])) + ']'

