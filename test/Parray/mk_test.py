import random

random.seed(0)

n = 5 * 10**5
q = 5 * 10**5
print(n, q)
A = [random.randrange(0, n) for _ in range(n)]
print(*A)
seen = set([-1])
for i in range(q):
    com = random.randint(0, 1)
    k = random.randrange(0, n)
    v = random.randrange(0, n)
    version = random.randrange(-1, i)
    while version not in seen:
        version = random.randrange(-1, i)
    if com == 0:  # get
        print(0, k, version)
    else:
        print(1, k, v, version)
        seen.add(i)
