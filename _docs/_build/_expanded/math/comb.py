# from titan_pylib.math.comb import Comb
class Comb:

    def __init__(self, n: int) -> int:
        self.n = n + 1
        table = [[0] * self.n for _ in range(self.n)]
        for i in range(self.n):
            for j in range(i + 1):
                if j == 0 or j == i:
                    table[i][j] = 1
                else:
                    table[i][j] = table[i - 1][j - 1] + table[i - 1][j]
        self.table = table

    def nCr(self, n: int, r: int) -> int:
        return self.table[n][r]
