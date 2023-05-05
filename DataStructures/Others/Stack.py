from typing import Iterable

class Stack:

  # コンセプト：popをしないStack

  def __init__(self, a: Iterable=[]):
    self.data = list(a)
    self.back = len(self.data)

  def pop(self):
    self.back -= 1
    return self.data[self.back]

  def append(self, val):
    if self.back < len(self.data):
      self.data[self.back] = val
    else:
      self.data.append(val)
    self.back += 1

  def top(self):
    return self.data[self.back-1]

  def count(self, key):
    return self.data.count(key)

  def __getitem__(self, k: int):
    if k < 0: k += self.back
    return self.data[k]

  def __contains__(self, val):
    return val in self.data

  def __iter__(self):
    self.__iter = -1
    return self

  def __next__(self):
    if self.__iter+1 >= self.back:
      raise StopIteration
    self.__iter += 1
    return self.data[self.__iter]

  def __len__(self):
    return self.back

  def __str__(self):
    return '[' + ', '.join(map(str, self)) + ']'

  def __repr__(self):
    return f'Stack({self})'

