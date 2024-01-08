from titan_pylib.data_structures.set.wordsize_tree_set import WordsizeTreeSet
from a import MyWordsizeTreeSet

u = 10**7
# ans = WordsizeTreeSet(u)

from time import process_time
import random
random.seed(0)

m = 10

# start = process_time()
# for _ in range(m):
#   for i in range(u):
#     ans.add(i)
#   ans.tolist()
# print(process_time() - start)

test = MyWordsizeTreeSet(u)
start = process_time()
for _ in range(m):
  for i in range(u):
    test.add(i)
  test.tolist()
print(process_time() - start)
exit()

from time import process_time

def bit_length64(x: int) -> int:
  # return x.bit_length() if x < 4294967296 else (x>>32).bit_length() + 32

  x |= x >> 1
  x |= x >> 2
  x |= x >> 4
  x |= x >> 8
  x |= x >> 16
  x |= x >> 32
  x = x - ((x >> 1) & 0x5555555555555555)
  x = (x & 0x3333333333333333) + ((x >> 2) & 0x3333333333333333)
  x = (x + (x >> 4)) & 0x0f0f0f0f0f0f0f0f
  x = x + (x >> 8)
  x = x + (x >> 16)
  x = x + (x >> 32)
  return x & 0x0000007f

start = process_time()
for i in range(10**8):
  a = 1 << (i % 63)
  x = bit_length64(a)
print(process_time() - start)

# import dis
# def main():
#   x.bit_length()

# dis.dis(main)
