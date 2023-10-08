from typing import Dict, Iterable, List, Optional, TypeVar, Generic
T = TypeVar('T')

class PersistentStack(Generic[T]):

  class Node():

    def __init__(self, key: Optional[T], prev=None):
      self.key: Optional[T] = key
      self.prev: Optional[PersistentStack.Node] = prev

  def __init__(self, a: Iterable[T]=[], init_t: int=-1, _prev: Optional['PersistentStack']=None):
    self.prev: Optional[PersistentStack] = _prev
    stack = PersistentStack.Node(None, None)
    for e in a:
      stack = PersistentStack.Node(e, prev=stack)
    self.a: Dict[int, PersistentStack.Node] = {init_t: stack}

  def top(self, t: int) -> T:
    res = self.a[t].key
    assert res is not None, f'IndexError: top from empty stack'
    return res

  def append(self, key: T, pre_t: int, new_t: int) -> None:
    s = self.a[pre_t]
    new_stack = PersistentStack.Node(key, s)
    self.a[new_t] = new_stack

  def pop(self, pre_t: int, new_t: int) -> T:
    s = self.a[pre_t]
    assert s.key is not None, f'IndexError: pop from empty stack'
    self.a[new_t] = PersistentStack.Node(None) if s.prev is None else s.prev
    return s.key

  def tolist(self, t: int) -> List[T]:
    a = []
    stack = self.a[t]
    while stack.prev is not None:
      a.append(stack.key)
      stack = stack.prev
    return a[::-1]

