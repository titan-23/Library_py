from PersistentArray32 import PersistentArray32

# from PersistentArray import PersistentArray
from time import process_time
import sys

input = lambda: sys.stdin.buffer.readline().rstrip()

# n = 10
# a = PersistentArray(range(n))
# print([a[i] for i in range(n)])
# exit()

from pyrsistent import v, pvector

m = 3
n, q = map(int, input().split())
A = list(map(int, input().split()))
query = [tuple(map(int, input().split())) for _ in range(q)]

start = process_time()
for _ in range(m):
    pA = [None] * (q + 1)
    vA = [None] * (q + 1)

    pA[-1] = PersistentArray32(A)
    vA[-1] = pvector(A)

    i = 0
    for com, *qu in query:
        if com == 0:
            k, version = qu
            vA[version][k]
            pA[version][k]
            assert pA[version][k] == vA[version][k]
        else:
            k, v, version = qu
            vA[i] = vA[version].set(k, v)
            pA[i] = pA[version].set(k, v)
        i += 1
print(f"{(process_time() - start)/m:.6f}sec", file=sys.stderr)
