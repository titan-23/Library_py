import math
from typing import Union, Optional
from titan_pylib.algorithm.sort.merge_sort import merge_sort
from decimal import Decimal

# GEO_EPS = Decimal("1e-8")
GEO_EPS = 1e-8


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
        if Geometry._lt(self.x, other.x):
            return True
        if Geometry._lt(other.x, self.x):
            return False
        return Geometry._lt(self.y, other.y)

    def __lt__(self, other: "Point") -> bool:
        if self == other:
            return False
        if Geometry._lt(self.x, other.x):
            return True
        if Geometry._lt(other.x, self.x):
            return False
        return Geometry._lt(self.y, other.y)

    def __ge__(self, other: "Point") -> bool:
        return not (self < other)

    def __gt__(self, other: "Point") -> bool:
        return not (self <= other)

    def __eq__(self, other: "Point") -> bool:
        return abs(self.x - other.x) < GEO_EPS and abs(self.y - other.y) < GEO_EPS

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


class Segment:

    def __init__(self, p1: Point, p2: Point) -> None:
        if p1 > p2:
            p1, p2 = p2, p1
        self.p1 = p1
        self.p2 = p2


class Polygon:
    """多角形クラス"""

    def __init__(self, ps: list[Point]) -> None:
        self.n = len(ps)
        self.ps = sorted(Geometry.argumant_sort(ps))

    def area(self) -> float:
        """面積を求める / `O(n)`

        Returns:
            float: 面積
        """
        res = 0.0
        p = self.ps
        for i in range(self.n - 1):
            res += Geometry.cross(p[i], p[i + 1])
        res += Geometry.cross(p[-1], p[0])
        return res * 0.5

    def is_convex(self) -> bool:
        """凸多角形かどうか / `O(n)`

        Returns:
            bool:
        """
        ps = self.ps
        for i in range(self.n):
            pre = (i - 1 + self.n) % self.n
            now = i
            nxt = (i + 1) % self.n
            if Geometry.ccw(ps[pre], ps[now], ps[nxt]) == -1:
                return False
        return True

    def contains(self, p: Point) -> int:
        """点の包含関係を返す

        Args:
            p (Point): 点

        Returns:
            int: `2`: `p` を含む
                 `1`: `p` が辺上にある
                 `0`: それ以外
        """
        is_in = False
        ps = self.ps
        EPS = GEO_EPS
        for i in range(self.n):
            a = ps[i] - p
            b = ps[(i + 1) % self.n] - p
            if a.y > b.y:
                a, b = b, a
            if a.y < EPS and EPS < b.y and Geometry.cross(a, b) < -EPS:
                is_in = not is_in
            if Geometry._eq(Geometry.cross(a, b), 0) and Geometry.dot(a, b) < EPS:
                return 1
        return 2 if is_in else 0

    def convex_hull(self, line_contains: bool = False) -> list[Point]:
        """凸包を求める / `O(n)`

        Args:
            line_contains (bool, optional): 一直線上の点を含める場合、 `True` .

        Returns:
            list[Point]: 凸包
        """
        ps = Geometry.sort_by_y(self.ps)
        if not line_contains:
            ps = Geometry.unique(ps)
        if len(ps) <= 1:
            return ps

        def cross(a, p):
            if line_contains:
                return Geometry.cross(a[-1] - a[-2], p - a[-1]) < -GEO_EPS
            else:
                return Geometry.cross(a[-1] - a[-2], p - a[-1]) < GEO_EPS

        lower = []
        for p in ps:
            while len(lower) > 1 and cross(lower, p):
                lower.pop()
            lower.append(p)

        upper = []
        for p in reversed(ps):
            while len(upper) > 1 and cross(upper, p):
                upper.pop()
            upper.append(p)

        return lower[:-1] + upper[:-1]

    def diameter(self) -> Optional[tuple[float, int, int]]:
        ch = self.convex_hull()
        n = len(ch)
        if n == 0:
            return None
        if n == 1:
            return 0, ch[0], ch[0]
        if n == 2:
            return abs(ch[0] - ch[1]), ch[0], ch[1]
        u, v = 0, 0
        up, vp = None, None
        for i in range(n):
            if ch[u] > ch[i]:
                u = i
                up = ch[i]
            if ch[v] < ch[i]:
                v = i
                vp = ch[i]
        d = 0
        su, sv = u, v
        loop = False
        while (u != su or v != sv) or (not loop):
            loop = True
            if Geometry._lt(d, abs(ch[u] - ch[v])):
                d = abs(ch[u] - ch[v])
                up = ch[u]
                vp = ch[v]
            if Geometry._lt(
                Geometry.cross(ch[(u + 1) % n] - ch[u], ch[(v + 1) % n] - ch[v]), 0
            ):
                u = (u + 1) % n
            else:
                v = (v + 1) % n
        return d, up, vp


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


class Geometry:
    """ref:
    - https://hcpc-hokudai.github.io/archive/geometry_004.pdf
    - https://bakamono1357.hatenablog.com/entry/2020/04/29/025320
    - https://tjkendev.github.io/procon-library/python/geometry/circles_associated_with_triangle.html
    """

    @classmethod
    def _eq(cls, a: float, b: float) -> bool:
        return abs(a - b) < GEO_EPS

    @classmethod
    def dot(cls, p1: Point, p2: Point) -> float:
        return p1.x * p2.x + p1.y * p2.y

    @classmethod
    def cross(cls, p1: Point, p2: Point) -> float:
        return p1.x * p2.y - p1.y * p2.x

    @classmethod
    def ccw(cls, u: Point, v: Point, p: Point) -> int:
        """u->vに対し、v->pの位置関係を求める

        Args:
            u (Point):
            v (Point):
            p (Point):

        Returns:
            int: `+1`: a->bに対し、b->cが半時計回りに進む
                 `-1`: a->bに対し、b->cが時計回りに進む
                 `+2`: a->bに対し、b->cが逆方向に進む
                 `-2`: a->bに対し、b->cが同一方向に進む
                 ` 0`: cが線分a->b上にある
        """
        if cls.cross(v - u, p - u) > GEO_EPS:
            return 1
        if cls.cross(v - u, p - u) < -GEO_EPS:
            return -1
        if cls.dot(v - u, p - u) < -GEO_EPS:
            return 2
        if Geometry._lt(abs(v - u), abs(p - u)):
            # if abs(v - u) + GEO_EPS < abs(p - u):
            return -2
        return 0

    @classmethod
    def projection_point(cls, p: Point, l: Line) -> Point:
        """直線 `l` に、点 `p` からおろした垂線の足の `Point` を返す

        Args:
            p (Point): 点
            l (Line): 直線

        Returns:
            Point:
        """
        t = cls.dot(p - l.p1, l.p1 - l.p2) / (l.p1 - l.p2).norm2()
        return l.p1 + (l.p1 - l.p2) * t

    @classmethod
    def reflection_point(cls, p: Point, l: Line) -> Point:
        """直線 `l` を対象軸として点 `p` と線対称の点を返す

        Args:
            p (Point): 点
            l (Line): 直線

        Returns:
            Point:
        """
        return p + 2 * (cls.projection_point(p, l) - p)

    @classmethod
    def is_orthogonal(cls, l1: Line, l2: Line) -> bool:
        """直線 `l1, l2` が直行しているかどうか

        Args:
            l1 (Line): 直線
            l2 (Line): 直線

        Returns:
            bool:
        """
        return cls._eq(cls.dot(l1.p2 - l1.p1, l2.p2 - l2.p1), 0)

    @classmethod
    def is_parallel(cls, l1: Line, l2: Line) -> bool:
        """直線 `l1, l2` が平行かどうか

        Args:
            l1 (Line): 直線
            l2 (Line): 直線

        Returns:
            bool:
        """
        return cls._eq(cls.cross(l1.p2 - l1.p1, l2.p2 - l2.p1), 0)

    @classmethod
    def is_intersect_linesegment(cls, s1: Segment, s2: Segment) -> bool:
        """線分 `s1` と `s2` が交差しているかどうか判定する

        Args:
            s1 (Segment): 線分
            s2 (Segment): 線分

        Returns:
            bool:
        """
        return (
            cls.ccw(s1.p1, s1.p2, s2.p1) * cls.ccw(s1.p1, s1.p2, s2.p2) <= 0
            and cls.ccw(s2.p1, s2.p2, s1.p1) * cls.ccw(s2.p1, s2.p2, s1.p2) <= 0
        )

    @classmethod
    def is_intersect_circle(cls, c1: Circle, c2: Circle) -> int:
        """2円の位置関係

        Args:
            c1 (Circle): 円
            c2 (Circle): 円

        Returns:
            int: 共通接線の数
                 `0`: 内包している
                 `1`: 内接している
                 `2`: 2点で交わっている
                 `3`: 外接している
                 `4`: 離れている
        """
        d = abs(c1.p - c2.p)
        if Geometry._gt(d, c1.r + c2.r):
            # if d > c1.r + c2.r + GEO_EPS:
            return 4
        if cls._eq(d, c1.r + c2.r):
            return 3
        if cls._eq(d, abs(c1.r - c2.r)):
            return 1
        if Geometry._lt(d, abs(c1.r - c2.r)):
            # if d < abs(c1.r - c2.r) - GEO_EPS:
            return 0
        return 2

    @classmethod
    def cross_point_segment(cls, s1: Segment, s2: Segment) -> Optional[Point]:
        d1 = cls.cross(s1.p2 - s1.p1, s2.p2 - s2.p1)
        d2 = cls.cross(s1.p2 - s1.p1, s1.p2 - s2.p1)
        if cls._eq(abs(d1), 0) and cls._eq(abs(d2), 0):
            return s2.p1
        if cls._eq(abs(d1), 0):
            return None
        return s2.p1 + (s2.p2 - s2.p1) * (d2 / d1)

    @classmethod
    def cross_point_circle(cls, c1: Circle, c2: Circle) -> tuple[Point, ...]:
        r = cls.is_intersect_circle(c1, c2)
        if r == 4 or r == 0:
            return ()
        if r == 3:  # 外接
            t = c1.r / (c1.r + c2.r)
            return (c1.p + (c2.p - c1.p) * t,)
        d = abs(c1.p - c2.p)
        if r == 1:  # 内接
            if Geometry._lt(c2.r, c1.r):
                # if c2.r < c1.r - GEO_EPS:
                return (c1.p + (c2.p - c1.p) * (c1.r / d),)
            else:
                return (c2.p + (c1.p - c2.p) * (c2.r / d),)
        # 交点が2つ
        rcos = (c1.r * c1.r + d * d - c2.r * c2.r) / (2 * d)
        rsin = math.sqrt(c1.r * c1.r - rcos * rcos)
        if Geometry._lt(c1.r - abs(rcos), 0):
            # if c1.r - abs(rcos) < GEO_EPS:
            rsin = 0
        e12 = (c2.p - c1.p) / abs(c2.p - c1.p)
        return tuple(
            sorted(
                [
                    c1.p + rcos * e12 + rsin * Point(-e12.y, e12.x),
                    c1.p + rcos * e12 + rsin * Point(e12.y, -e12.x),
                ]
            )
        )

    @classmethod
    def cross_point_circle_line(cls, c: Circle, l: Line) -> list[Point]:
        res = []
        d = cls.dist_p_to_line(c.p, l)
        if d > c.r + GEO_EPS:
            return res
        h = cls.projection_point(c.p, l)
        if cls._eq(d, c.r):
            res.append(h)
            return res
        e = (l.p2 - l.p1).unit()
        ph = math.sqrt(c.r * c.r - d * d)
        res.append(h - e * ph)
        res.append(h + e * ph)
        res.sort()
        return res

    @classmethod
    def dist_p_to_line(cls, p: Point, l: Line) -> float:
        return abs(cls.cross(l.p2 - l.p1, p - l.p1)) / abs(l.p2 - l.p1)

    @classmethod
    def dist_p_to_segmemt(cls, p: Point, s: Segment) -> float:
        if cls.dot(s.p2 - s.p1, p - s.p1) < GEO_EPS:
            return abs(p - s.p1)
        if cls.dot(s.p1 - s.p2, p - s.p2) < GEO_EPS:
            return abs(p - s.p2)
        return abs(cls.cross(s.p2 - s.p1, p - s.p1)) / abs(s.p2 - s.p1)

    @classmethod
    def dist_segment_to_segment(cls, s1: Segment, s2: Segment) -> float:
        if cls.is_intersect(s1, s2):
            return 0.0
        ans = float("inf")
        ans = min(ans, cls.dist_p_to_segmemt(s1.p1, s2))
        ans = min(ans, cls.dist_p_to_segmemt(s1.p2, s2))
        ans = min(ans, cls.dist_p_to_segmemt(s2.p1, s1))
        ans = min(ans, cls.dist_p_to_segmemt(s2.p2, s1))
        return ans

    @classmethod
    def triangle_incircle(cls, p1: Point, p2: Point, p3: Point) -> Circle:
        a, b, c = abs(p2 - p3), abs(p1 - p3), abs(p1 - p2)
        p = Point(a * p1.x + b * p2.x + c * p3.x, a * p1.y + b * p2.y + c * p3.y)
        p /= a + b + c
        d = cls.dist_p_to_segmemt(p, Line.from_points(p1, p2))
        return Circle(p, d)

    @classmethod
    def triangle_circumcircle(cls, p1: Point, p2: Point, p3: Point) -> Circle:
        a = 2 * (p1.x - p2.x)
        b = 2 * (p1.y - p2.y)
        p = p1.x**2 - p2.x**2 + p1.y**2 - p2.y**2
        c = 2 * (p1.x - p3.x)
        d = 2 * (p1.y - p3.y)
        q = p1.x**2 - p3.x**2 + p1.y**2 - p3.y**2
        u = a * d - b * c
        x = d * p - b * q
        y = a * q - c * p
        if Geometry._lt(u, 0):
            x = -x
            y = -y
            u = -u
        x /= u
        y /= u
        r = ((x - p1.x) ** 2 + (y - p1.y) ** 2) ** 0.5
        return Circle(Point(x, y), r)

    @classmethod
    def triangle_excircle(
        cls, p1: Point, p2: Point, p3: Point
    ) -> tuple[Circle, Circle, Circle]:
        dx1 = p2.x - p1.x
        dy1 = p2.y - p1.y
        dx2 = p3.x - p1.x
        dy2 = p3.y - p1.y
        d1 = ((p3.x - p2.x) ** 2 + (p3.y - p2.y) ** 2) ** 0.5
        d3 = (dx1**2 + dy1**2) ** 0.5
        d2 = (dx2**2 + dy2**2) ** 0.5
        S2 = abs(dx1 * dy2 - dx2 * dy1)
        dsum1 = -d1 + d2 + d3
        r1 = S2 / dsum1
        ex1 = (-p1.x * d1 + p2.x * d2 + p3.x * d3) / dsum1
        ey1 = (-p1.y * d1 + p2.y * d2 + p3.y * d3) / dsum1

        dsum2 = d1 - d2 + d3
        r2 = S2 / dsum2
        ex2 = (p1.x * d1 - p2.x * d2 + p3.x * d3) / dsum2
        ey2 = (p1.y * d1 - p2.y * d2 + p3.y * d3) / dsum2

        dsum3 = d1 + d2 - d3
        r3 = S2 / dsum3
        ex3 = (p1.x * d1 + p2.x * d2 - p3.x * d3) / dsum3
        ey3 = (p1.y * d1 + p2.y * d2 - p3.y * d3) / dsum3

        return (
            Circle(Point(ex1, ey1), r1),
            Circle(Point(ex2, ey2), r2),
            Circle(Point(ex3, ey3), r3),
        )

    @classmethod
    def circle_tangent(cls, p: Point, c: Circle) -> tuple[Point, Point]:
        return cls.cross_point_circle(
            c, Circle(p, math.sqrt((c.p - p).norm2() - c.r * c.r))
        )

    @classmethod
    def circle_common_tangent(cls, c1: Circle, c2: Circle) -> list[Line]:
        ret = []
        d = abs(c1.p - c2.p)
        if cls._eq(d, 0):
            return ret
        u = (c2.p - c1.p).unit()
        v = u.rotate(math.pi / 2)
        for s in [-1, 1]:
            h = (c1.r + c2.r * s) / d
            if cls._eq(h * h, 1):
                ret.append(
                    Line.from_points(
                        c1.p + (u if h > 0 else -u) * c1.r,
                        c1.p + (u if h > 0 else -u) * c1.r + v,
                    )
                )
            elif 1 - h * h > 0:
                U = u * h
                V = v * math.sqrt(1 - h * h)
                ret.append(
                    Line.from_points(c1.p + (U + V) * c1.r, c2.p - (U + V) * (c2.r * s))
                )
                ret.append(
                    Line.from_points(c1.p + (U - V) * c1.r, c2.p - (U - V) * (c2.r * s))
                )
        return ret

    @classmethod
    def unique(cls, a: list[Point]) -> list[Point]:
        """同一要素の削除

        Note:
            `a` は事前にソートされていなければいけません。

        Args:
            a (list[Point]):

        Returns:
            list[Point]:
        """
        if not a:
            return []
        res = [a[0]]
        for i in range(1, len(a)):
            if a[i] == res[-1]:
                continue
            res.append(a[i])
        return res

    @classmethod
    def _lt(cls, u: float, v: float) -> bool:
        return u < v and u < max(v, v - GEO_EPS)

    @classmethod
    def _gt(cls, u: float, v: float) -> bool:
        return u > v and u > min(v, v - GEO_EPS)

    @classmethod
    def argumant_sort(cls, a: list[Point]) -> list[Point]:
        upper = []
        lower = []
        zeros = []
        for p in a:
            if cls._lt(p.y, 0) or (cls._eq(p.y, 0) and cls._gt(p.x, 0)):
                lower.append(p)
            elif cls._eq(p.x, 0) and cls._eq(p.y, 0):
                zeros.append(p)
            else:
                upper.append(p)

        def cmp(s: Point, t: Point) -> bool:
            return cls._lt(s.y * t.x, s.x * t.y)

        upper = merge_sort(upper, key=cmp)
        lower = merge_sort(lower, key=cmp)
        return lower + zeros + upper

    @classmethod
    def sort_by_x(cls, a: list[Point]) -> list[Point]:
        return sorted(a)

    @classmethod
    def _cmp_y(cls, u: Point, v: Point):
        if cls._eq(u, v):
            return True
        if cls._lt(u.y, v.y):
            return True
        if cls._lt(v.y, u.y):
            return False
        return cls._lt(u.x, v.x)

    @classmethod
    def sort_by_y(cls, a: list[Point]) -> list[Point]:
        return merge_sort(a, cls._cmp_y)

    @classmethod
    def furthest_pair(cls, a: list[Point]) -> Optional[tuple[float, int, int]]:
        p = Polygon(a)
        d, up, vp = p.diameter()
        ui, vi = -1, -1
        for i, point in enumerate(a):
            if point == up:
                ui = i
        for i, point in enumerate(a):
            if i != ui and point == vp:
                vi = i
        assert ui != -1 and vi != -1
        return d, ui, vi

    @classmethod
    def closest_pair(cls, a: list[Point]) -> Optional[tuple[float, int, int]]:
        """最近点対を求める / O(nlogn)

        Args:
            a (list[Point]): 距離配列

        Returns:
            Optional[tuple[float, int, int]]: 距離、最近点対
        """

        buff = [0] * len(a)
        d = float("inf")
        p, q = -1, -1

        def f(l: int, r: int) -> None:
            nonlocal d, p, q
            mid = (l + r) // 2
            x = a[mid][0].x
            if mid - l > 1:
                f(l, mid)
            if r - mid > 1:
                f(mid, r)
            i, j = l, mid
            indx = 0
            while i < mid and j < r:
                if cls._cmp_y(a[i][0], a[j][0]):
                    buff[indx] = a[i]
                    i += 1
                else:
                    buff[indx] = a[j]
                    j += 1
                indx += 1
            for i in range(i, mid):
                buff[indx] = a[i]
                indx += 1
            for j in range(j, r):
                buff[indx] = a[j]
                indx += 1
            a[l:r] = buff[: r - l]

            near_line = []
            for i in range(l, r):
                e_p, e_i = a[i]
                v = abs(e_p.x - x)
                if cls._gt(v, d) or cls._eq(v, d):
                    continue
                for ne_p, ne_i in reversed(near_line):
                    dx = e_p.x - ne_p.x
                    dy = e_p.y - ne_p.y
                    if cls._gt(dy, d) or cls._eq(dy, d):
                        break
                    cand = math.sqrt(dx * dx + dy * dy)
                    if cls._lt(cand, d):
                        d = cand
                        p, q = ne_i, e_i
                near_line.append(a[i])

        if len(a) <= 1:
            return None
        a = sorted((e, i) for i, e in enumerate(a))
        f(0, len(a))
        return d, p, q


import sys

input = lambda: sys.stdin.readline().rstrip()

#  -----------------------  #


def solve():
    n = int(input())
    a = []
    for _ in range(n):
        x, y = map(int, input().split())
        a.append(Point(x, y))
    d, ui, vi = Geometry.furthest_pair(a)
    print(ui, vi)


t = int(input())
for _ in range(t):
    solve()
