# from titan_pylib.math.get_quotients import get_quotients
from typing import List


def get_quotients(n: int) -> List[int]:
    i = 1
    a = []
    while i * i <= n:
        a.append(n // i)
        a.append(n // (n // i))
        i += 1
    a.sort()
    if not a:
        return a
    b = [a[0]]
    for i in range(1, len(a)):
        if b[-1] != a[i]:
            b.append(a[i])
    return b
