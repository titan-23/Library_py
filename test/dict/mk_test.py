import random

random.seed(0)

q = 10**6
print(q)
for _ in range(q):
    com = random.randint(0, 1)
    key = random.randint(0, 10**18)
    val = random.randint(0, 10**18)
    if com == 0:  # set
        print(com, key, val)
    else:
        print(com, key)
