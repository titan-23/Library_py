from titan_pylib.geometry.polygon import Polygon
from titan_pylib.geometry.point import Point
from titan_pylib.geometry.geometry import Geometry
from titan_pylib.geometry.geometry_util import GeometryUtil


class ConvecPolygon(Polygon):

    def __init__(self, ps: list[Point]) -> None:
        self.n = len(ps)
        self.ps = Geometry.convex_hull(ps)

    def diameter(self) -> tuple[float, int, int]:
        ps = self.ps
        n = len(ps)
        if n == 0:
            return -1, -1, -1
        if n == 1:
            return 0, ps[0], ps[0]
        if n == 2:
            return abs(ps[0] - ps[1]), ps[0], ps[1]
        u, v = 0, 0
        up, vp = None, None
        for i in range(n):
            if ps[u] > ps[i]:
                u = i
                up = ps[i]
            if ps[v] < ps[i]:
                v = i
                vp = ps[i]
        d = 0
        su, sv = u, v
        loop = False
        while (u != su or v != sv) or (not loop):
            loop = True
            if GeometryUtil.lt(d, abs(ps[u] - ps[v])):
                d = abs(ps[u] - ps[v])
                up = ps[u]
                vp = ps[v]
            if GeometryUtil.lt(
                Geometry.cross(ps[(u + 1) % n] - ps[u], ps[(v + 1) % n] - ps[v]), 0
            ):
                u = (u + 1) % n
            else:
                v = (v + 1) % n
        return d, up, vp

    def contains(self, p: Point) -> int:
        """点の包含関係を返す / O(n)

        Args:
            p (Point): 点

        Returns:
            int: `2`: `p` を含む
                 `1`: `p` が辺上にある
                 `0`: それ以外
        """
        ps = self.ps
        n = len(ps)
        b1 = Geometry.cross(ps[1] - ps[0], p - ps[0])
        b2 = Geometry.cross(ps[-1] - ps[0], p - ps[0])
        if GeometryUtil.lt(b1, 0) or GeometryUtil.gt(b2, 0):
            return 0
        l, r = 1, n - 1
        while r - l > 1:
            mid = (l + r) >> 1
            c = Geometry.cross(p - ps[0], ps[mid] - ps[0])
            if GeometryUtil.eq(c, 0) or GeometryUtil.gt(c, 0):
                r = mid
            else:
                l = mid
        b3 = Geometry.cross(ps[l] - p, ps[r] - p)
        if GeometryUtil.eq(b3, 0):
            return 1
        if GeometryUtil.gt(b3, 0):
            if GeometryUtil.eq(b1, 0) or GeometryUtil.eq(b2, 0):
                return 1
            else:
                return 2
        return 0
