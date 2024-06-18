# from titan_pylib.geometry.gomi.geometry_util import GeometryUtil
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

    @classmethod
    def le(cls, u: float, v: float) -> bool:
        return not cls.gt(u, v)

    @classmethod
    def ge(cls, u: float, v: float) -> bool:
        return not cls.lt(u, v)
