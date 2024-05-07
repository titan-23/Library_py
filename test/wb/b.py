import random


def isbug():
    q = 100
    M = 30

    print(0, q)
    print()
    now = []
    unused = list(range(M))
    for _ in range(q):
        com = random.randint(0, 1)
        if not now:
            com = 0
        if not unused:
            com = 1

        if com == 0:
            x = random.choice(unused)
            unused.remove(x)
            now.append(x)
            print(com, x)
        else:
            x = random.choice(now)
            unused.append(x)
            now.remove(x)
            print(com, x)


def P():
    n = 2 * 10**5
    k = 10**5
    P = list(range(1, n + 1))
    random.shuffle(P)
    print(n, k)
    print(*P)


def sequence_query():
    q = 2 * 10**5
    print(q)
    for _ in range(q):
        com = random.randint(1, 3)
        x = random.randint(1, 10**18)
        k = 5
        if com == 1:
            print(com, x)
        elif com == 2:
            print(com, x, k)
        else:
            print(com, x, k)


# P()
sequence_query()
