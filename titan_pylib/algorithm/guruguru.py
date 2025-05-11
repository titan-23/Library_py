def guruguru(n):
    dx = (0, 1, 0, -1)
    dy = (-1, 0, 1, 0)
    A = [[0] * n for _ in range(n)]
    i, j = n // 2, n // 2
    if n % 2 == 0:
        j -= 1
    m = n * n
    l = 1
    val = 1
    while val < m:
        for k in range(4):
            for t in range(l):
                i += dy[k]
                j += dx[k]
                if 0 <= i < n and 0 <= j < n:
                    A[i][j] = val
                    val += 1
            if k % 2 == 1:
                l += 1
    return A
