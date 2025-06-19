import random


def select_k_random(n: int, k: int) -> list[int]:
    if k > n or k < 0:
        raise ValueError("k must be between 0 and n")
    if k < n // 3:
        result = set()
        for j in range(n - k, n):
            t = random.randrange(j + 1)
            if t not in result:
                result.add(t)
            else:
                result.add(j)
        return sorted(result)
    else:
        result = list(range(0, k))
        for i in range(k, n):
            r = random.randint(0, i)
            if r < k:
                result[r] = i
        return sorted(result)
