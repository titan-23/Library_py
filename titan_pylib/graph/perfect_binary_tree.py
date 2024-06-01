class PerfectBinaryTree:

    def __init__(self) -> None:
        pass

    def par(self, u: int) -> int:
        return (u >> 1) if u > 1 else -1

    def child_left(self, u: int) -> int:
        return u << 1

    def child_right(self, u: int) -> int:
        return u << 1 | 1

    def children(self, u: int) -> tuple[int, int]:
        return (self.child_left(u), self.child_right(u))

    def sibling(self, u: int) -> int:
        return u ^ 1

    def dep(self, u: int) -> int:
        """:math:`O(1)`"""
        return u.bit_length()

    def la(self, u: int, k: int) -> int:
        """``k``個上の祖先
        k == 0 -> u
        """
        return u >> k

    def lca(self, u: int, v: int) -> int:
        if self.dep(u) > self.dep(v):
            u, v = v, u
        v = self.la(v, self.dep(v) - self.dep(u))
        return u >> (u ^ v).bit_length()

    def get_path(self, u: int, v: int) -> list[int]:
        def get(x):
            a = []
            while x != lca:
                a.append(x)
                x = self.par(x)
            return a

        lca = self.lca(u, v)
        return get(u) + [lca] + get(v)[::-1]
