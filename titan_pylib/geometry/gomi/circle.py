import math
from titan_pylib.geometry.point import Point


class Circle:

    __slots__ = "p", "r"

    def __init__(self, p: Point, r: float) -> None:
        """円

        Args:
            p (Point): 直径を表す `Point`
            r (float): 半径
        """
        self.p = p
        self.r = r

    def area(self) -> float:
        """面積を返す"""
        return math.pi * self.r * self.r
