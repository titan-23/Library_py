# from titan_pylib.others.fast_io import FastIO
import io, os

class FastIO():

  # https://recruit.gmo.jp/engineer/jisedai/blog/python_standard_io_with_bytesio/

  input_buf = io.BytesIO()
  output_buf = io.BytesIO()
  num_line = 0
  BUFSIZE = (1<<18)-1

  @classmethod
  def input(cls):
    pointer = cls.input_buf.tell()
    while cls.num_line == 0:
      byte_data = os.read(0, cls.BUFSIZE)
      cls.num_line = byte_data.count(b'\n') + (not byte_data)
      cls.input_buf.seek(0, 2)
      cls.input_buf.write(byte_data)
    cls.input_buf.seek(pointer)
    cls.num_line -= 1
    return cls.input_buf.readline().decode().rstrip()

  @classmethod
  def buf_input(cls):
    pointer = cls.input_buf.tell()
    while cls.num_line == 0:
      byte_data = os.read(0, cls.BUFSIZE)
      cls.num_line = byte_data.count(b"\n") + (not byte_data)
      cls.input_buf.seek(0, 2)
      cls.input_buf.write(byte_data)
    cls.input_buf.seek(pointer)
    cls.num_line -= 1
    return cls.input_buf.readline()

  @classmethod
  def write(cls, *args, sep=' ', end='\n', flush=False):
    for i in range(len(args)-1):
      cls.output_buf.write(str(args[i]).encode())
      cls.output_buf.write(sep.encode())
    if args:
      cls.output_buf.write(str(args[-1]).encode())
    cls.output_buf.write(end.encode())
    if flush:
      cls.flush()

  @classmethod
  def flush(cls):
    os.write(1, cls.output_buf.getvalue())
    cls.output_buf.truncate(0)
    cls.output_buf.seek(0)

buf_input = FastIO.buf_input
input = FastIO.input
write = FastIO.write
flush = FastIO.flush

