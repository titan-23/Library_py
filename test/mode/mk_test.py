import random

n = 10**5
q = 10**5
u = 10**3

print(n, q)
print(*[random.randrange(0, u) for _ in range(n)])

for _ in range(q):
  l = random.randrange(0, n-100)
  r = l + random.randrange(1, 100)
  # while l == r:
  #   r = random.randrange(0, n)
  # if l > r:
  #   l, r = r, l
  print(l, r)
