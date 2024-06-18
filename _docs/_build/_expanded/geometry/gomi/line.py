# 展開に失敗しました
import math
from titan_pylib.geometry.point import Point


class Line:
    """ax + by + c = 0"""

    __slots__ = "a", "b", "c", "p1", "p2"

    def __init__(self, a: int, b: int, c: int, p1: Point, p2: Point) -> None:
        self.a = a
        self.b = b
        self.c = c
        self.p1 = p1
        self.p2 = p2

    @classmethod
    def from_points(cls, p1: Point, p2: Point) -> "Line":
        a = p2.y - p1.y
        b = p1.x - p2.x
        c = -p1.y * b - p1.x * a
        if isinstance(a, int) and isinstance(b, int) and isinstance(c, int):
            g = math.gcd(a, b)
            g = math.gcd(g, c)
            a //= g
            b //= g
            c //= g
        a, b, c = max((a, b, c), (-a, -b, -c))
        return cls(a, b, c, p1, p2)

    @classmethod
    def from_abc(cls, a: int, b: int, c: int) -> "Line":
        raise NotImplementedError
