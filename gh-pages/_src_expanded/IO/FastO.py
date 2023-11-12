# from Library_py.IO.FastO import FastO
import os
from __pypy__.builders import StringBuilder

class FastO():

  sb = StringBuilder()

  @classmethod
  def write(cls, *args, sep: str=' ', end: str='\n', flush: bool=False) -> None:
    append = cls.sb.append
    for i in range(len(args)-1):
      append(str(args[i]))
      append(sep)
    if args:
      append(str(args[-1]))
    append(end)
    if flush:
      cls.flush()

  @classmethod
  def flush(cls) -> None:
    os.write(1, cls.sb.build().encode())
    cls.sb = StringBuilder()


