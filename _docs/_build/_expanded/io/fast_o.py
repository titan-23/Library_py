# from titan_pylib.io.fast_o import FastO
import os
from __pypy__.builders import StringBuilder

class FastO():
  """標準出力高速化ライブラリです。
  """

  _sb = StringBuilder()

  @classmethod
  def write(cls, *args, sep: str=' ', end: str='\n', flush: bool=False) -> None:
    """標準出力します。次の ``FastO.flush()`` が起きると print します。
    """
    append = cls._sb.append
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
    """``flush`` します。これを実行しないと ``write`` した内容が表示されないので忘れないでください。
    """
    os.write(1, cls._sb.build().encode())
    cls._sb = StringBuilder()


