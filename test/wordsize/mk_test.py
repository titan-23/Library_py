import random

random.seed(0)

n = 10**7
q = 10**6
print(n, q)
s = [random.randint(0, 1) for _ in range(n)]
print("".join(map(str, s)))
for i in range(q):
    com = random.randint(0, 4)
    k = random.randrange(0, n)
    print(com, k)
