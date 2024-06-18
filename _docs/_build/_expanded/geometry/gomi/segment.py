# 展開に失敗しました
from titan_pylib.geometry.point import Point


class Segment:

    def __init__(self, p1: Point, p2: Point) -> None:
        if p1 > p2:
            p1, p2 = p2, p1
        self.p1 = p1
        self.p2 = p2
