from titan_pylib.data_structures.cumulative_sum.cumulative_sum import CumulativeSum


class CycleCumsum:

    def __init__(self, a, k):
        self.a = a
        self.n = len(a)
        self.k = k
        self.acc = CumulativeSum(a)

    def prod(self, l, r):
        assert 0 <= l <= r <= self.n * self.k
        nl = l // self.n
        nr = r // self.n
        il = l % self.n
        ir = r % self.n
        s = 0
        if nl == nr:
            s += self.acc.sum(il, ir)
        else:
            s += self.acc.sum(il, self.n)
            s += self.acc.sum(0, self.n) * (nr - nl - 1)
            s += self.acc.sum(0, ir)
        return s
