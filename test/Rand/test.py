from Random import Random

from time import process_time
import sys

q = 10**8
n = 10**9
start = process_time()
for _ in range(q):
  pass
t = process_time() - start

start = process_time()
for _ in range(q):
  Random.randint(0, n)
print(process_time() - start - t, file=sys.stderr)
