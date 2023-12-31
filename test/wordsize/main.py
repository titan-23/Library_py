
from time import process_time
import sys

input = lambda: sys.stdin.readline().rstrip()

from Library_py.DataStructures.RedBlackTree.RedBlackTreeSet import RedBlackTreeSet

#  -----------------------  #

start = process_time()
n, q = map(int, input().split())
S = input()
s = WordsizeTreeSet(n, (i for i, c in enumerate(S) if c == '1'))
# avl = RedBlackTreeSet(i for i, c in enumerate(S) if c == '1')
for _ in range(q):
  c, k = map(int, input().split())
  if c == 0:
    s.add(k)
    # avl.add(k)
  elif c == 1:
    s.discard(k)
    # avl.discard(k)
  elif c == 2:
    x = (1 if k in s else 0)
    print(x)
    # y = (1 if k in avl else 0)
    # assert x == y
  elif c == 3:
    ans1 = s.ge(k)
    print(ans1)
    # ans2 = avl.ge(k)
    # assert ans1 == ans2, f'{ans1=}, {ans2=}'
  else:
    ans1 = s.le(k)
    print(ans1)
    # ans2 = avl.le(k)
    # assert ans1 == ans2, f'{ans1=}, {ans2=}'
print(process_time() - start, file=sys.stderr)
