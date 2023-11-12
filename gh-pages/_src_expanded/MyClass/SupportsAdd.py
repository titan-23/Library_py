# from Library_py.MyClass.SupportsAdd import SupportsAdd
from typing import Protocol

class SupportsAdd(Protocol):

  def __add__(self, other): ...
  def __iadd__(self, other): ...
  def __radd__(self, other): ...


