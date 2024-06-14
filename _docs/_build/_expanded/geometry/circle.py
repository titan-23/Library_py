# from titan_pylib.geometry.circle import Circle
import math
# from titan_pylib.geometry.point import Point
import math
from typing import Union
# from titan_pylib.geometry.geometry_util import GeometryUtil
from typing import Final
from decimal import Decimal


class GeometryUtil:

    GEO_EPS: Final[float] = 1e-8

    @classmethod
    def eq(cls, a: float, b: float) -> bool:
        return abs(a - b) < cls.GEO_EPS

    @classmethod
    def lt(cls, u: float, v: float) -> bool:
        return u < v and u < max(v, v - cls.GEO_EPS)

    @classmethod
    def gt(cls, u: float, v: float) -> bool:
        return u > v and u > min(v, v - cls.GEO_EPS)


class Point:

    __slots__ = "x", "y"

    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f"Point({self.x}, {self.y})"

    __repr__ = __str__

    def show(self, precision: int = 16) -> None:
        format_string = f"{{:.{precision}f}}"
        print(f"{format_string.format(self.x)} {format_string.format(self.y)}")

    def __add__(self, other: "Point") -> "Point":
        if isinstance(other, Point):
            return Point(self.x + other.x, self.y + other.y)
        else:
            return Point(self.x + other, self.y + other)

    def __sub__(self, other: Union["Point", float]) -> "Point":
        if isinstance(other, Point):
            return Point(self.x - other.x, self.y - other.y)
        else:
            return Point(self.x - other, self.y - other)

    def __mul__(self, other: Union["Point", float]) -> "Point":
        if isinstance(other, Point):
            return Point(self.x * other.x, self.y * other.y)
        else:
            return Point(self.x * other, self.y * other)

    __rmul__ = __mul__

    def __truediv__(self, other: float) -> "Point":
        return Point(self.x / other, self.y / other)

    def __le__(self, other: "Point") -> bool:
        if self == other:
            return True
        if GeometryUtil.lt(self.x, other.x):
            return True
        if GeometryUtil.lt(other.x, self.x):
            return False
        return GeometryUtil.lt(self.y, other.y)

    def __lt__(self, other: "Point") -> bool:
        if self == other:
            return False
        if GeometryUtil.lt(self.x, other.x):
            return True
        if GeometryUtil.lt(other.x, self.x):
            return False
        return GeometryUtil.lt(self.y, other.y)

    def __ge__(self, other: "Point") -> bool:
        return not (self < other)

    def __gt__(self, other: "Point") -> bool:
        return not (self <= other)

    def __eq__(self, other: "Point") -> bool:
        return (
            abs(self.x - other.x) < GeometryUtil.GEO_EPS
            and abs(self.y - other.y) < GeometryUtil.GEO_EPS
        )

    def __neg__(self) -> "Point":
        return Point(-self.x, -self.y)

    def __abs__(self) -> float:
        return math.sqrt(self.x * self.x + self.y * self.y)

    def norm(self) -> float:
        """norm"""
        return abs(self)

    def norm2(self) -> float:
        """(x**2 + y**2)を返す(ルートの計算はしない)"""
        return self.x * self.x + self.y * self.y

    def unit(self) -> "Point":
        return self / abs(self)

    def rotate(self, theta: float) -> "Point":
        return Point(
            math.cos(theta) * self.x - math.sin(theta) * self.y,
            math.sin(theta) * self.x + math.cos(theta) * self.y,
        )


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
