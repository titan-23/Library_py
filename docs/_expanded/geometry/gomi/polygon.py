# 展開に失敗しました
from titan_pylib.geometry.point import Point
from titan_pylib.geometry.geometry import Geometry


class Polygon:
    """多角形クラス"""

    def __init__(self, ps: list[Point]) -> None:
        self.n = len(ps)
        self.ps = ps

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
        ps = self.ps
        cnt = 0
        for i in range(self.n - 1):
            if (ps[i].y <= p.y) and (ps[i + 1].y > p.y):
                vt = (p.y - ps[i].y) / (ps[i + 1].y - ps[i].y)
                if p.x < (ps[i].x + (vt * (ps[i + 1].x - ps[i].x))):
                    cnt += 1
            elif (ps[i].y > p.y) and (ps[i + 1].y <= p.y):
                vt = (p.y - ps[i].y) / (ps[i + 1].y - ps[i].y)
                if p.x < (ps[i].x + (vt * (ps[i + 1].x - ps[i].x))):
                    cnt -= 1
        return cnt
