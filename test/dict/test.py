# from Library_py.DataStructures.Dict.HashDict import HashDict
from dic import HashDict
from time import process_time
import sys
input = lambda: sys.stdin.buffer.readline().rstrip()

m = 10
q = int(input())
query = [tuple(map(int, input().split())) for _ in range(q)]

start = process_time()
for _ in range(m):
  d = HashDict()
  for com, *qu in query:
    if com == 0:
      key, val = qu
      d[key] = val
    else:
      key = qu[0]
      d.get(key, 0)
print(f'{(process_time() - start)/m:.6f}sec', file=sys.stderr)
# 0.859375sec
