#######################
"2つの座標を通る直線をtuple(一意)として表す"
# tyokusennnosiki chokusennnosiki line houteisiki
# 各座標は整数値

import math
def line(x1:int, y1:int, x2:int, y2:int) -> tuple:
  a = y2 - y1
  b = x1 - x2
  c = -y1*b - x1*a
  g = math.gcd(a, b)
  g = math.gcd(g, c)
  a //= g
  b //= g 
  c //= g 
  return max((a, b, c),  (-a, -b, -c))

#######################

def circles_cross_points(x1, y1, r1, x2, y2, r2):
  rr0 = (x2 - x1)**2 + (y2 - y1)**2
  if rr0 > (r1+r2)**2:
    return None
  xd = x2 - x1
  yd = y2 - y1
  rr1 = r1**2; rr2 = r2**2
  cv = (rr0 + rr1 - rr2)
  sv = (4*rr0*rr1 - cv**2)**.5
  return tuple(sorted([
    (x1 + (cv*xd - sv*yd)/(2*rr0), y1 + (cv*yd + sv*xd)/(2*rr0)),
    (x1 + (cv*xd + sv*yd)/(2*rr0), y1 + (cv*yd - sv*xd)/(2*rr0))
  ]))

def circle_tangent_points(x1, y1, r1, x2, y2):
  dd = (x1 - x2)**2 + (y1 - y2)**2
  r2 = (dd - r1**2) ** 0.5
  return circles_cross_points(x1, y1, r1, x2, y2, r2)

#######################
#"面積最大の正方形を求める"
# xy = [tuple(map(int, input().split())) for _ in range(n)]
# st = set(xy)
# ans = 0
# for i in range(n):
#   for j in range(i+1, n):
#     if (xy[i][0]-(xy[j][1]-xy[i][1]), xy[i][1]+xy[j][0]-xy[i][0]) in st and (xy[j][0]-(xy[j][1]-xy[i][1]), xy[j][1]+xy[j][0]-xy[i][0]) in st:
#       ans = max(ans, (xy[j][0]-xy[i][0])**2+(xy[j][1]-xy[i][1])**2)
# print(ans)
#######################
import math
def rotate(a, b, d, rad=True):
  if not rad:
    d = math.radians(d)
  x = a * math.cos(d) - b * math.sin(d)
  y = a * math.sin(d) + b * math.cos(d)
  return (x, y)

#######################
"区間[l1, r1], [l2, r2]が共通部分を持つか"
#kukangakyoutuububunnwomotuka
def have_intersection(l1, r1, l2, r2):
  if l1 > r1:
    l1, r1 = r1, l1 
  if l2 > r2:
    l2, r2 = r2, l2
  return (l1 <= l2 <= r1) or (l2 <= l1 <= r2)

#######################
# p(x, y, )から、直線lp((x, y, ), (x, y, ))に
# おろした垂線の足の座標

def get_projection_point(p: tuple, lp: tuple) -> tuple:
  dim = len(p)
  sta = lp[0]
  p = [p[i] - lp[0][i] for i in range(dim)]
  lp_ = []
  for i in range(2):
    lp_.append([lp[i][j] - lp[0][j] for j in range(dim)])
  lp = lp_
  vec = [q2 - q1 for q1,q2 in zip(*lp)]
  bunshi, bunbo = 0, 0
  for i in range(dim):
    bunshi += vec[i] * p[i]
    bunbo  += vec[i] * vec[i]
  k = bunshi / bunbo
  return tuple([k*vec[i]+sta[i] for i in range(dim)])

#######################
# (直線 lp に対する点 pの反射)
def get_reflection_point(p: tuple, lp: tuple) -> tuple:
  dim = len(p)
  proj = get_projection_point(p, lp)
  return tuple([p[i] + 2*(proj[i]-p[i]) for i in range(dim)])

#######################
#
def is_orthogonal_parallel(l1: tuple, l2: tuple) -> int:
  # li: line, l2: line
  # 直行: 1
  # 平行: 2
  # それ以外: 0
  if l1[0]*l2[0] + l1[1]*l2[1] == 0:
    return 1
  elif l1[0]*l2[1] - l1[1]*l2[0] == 0:
    return 2
  else:
    return 0

#######################

def area_three_points(x1, y1, x2, y2, x3, y3):
  x1 -= x3; x2 -= x3; y1 -= y3; y2 -= y3
  return abs(x1*y2 - x2*y1) / 2

#######################

# 点x, yと直線lpとの距離D
def get_dist(x, y, lp):
  return abs(x*lp[0] + y*lp[1] + lp[2]) / (lp[0]*lp[0] + lp[1]*lp[1])**.5

#######################

class LineSegmentIntersect:
  # 線分同士の交点判定
  
  def _dot(self, O, A, B):
    ox, oy = O
    ax, ay = A
    bx, by = B
    return (ax - ox) * (bx - ox) + (ay - oy) * (by - oy)
  
  def _cross(self, O, A, B):
    ox, oy = O
    ax, ay = A
    bx, by = B
    return (ax - ox) * (by - oy) - (bx - ox) * (ay - oy)
  
  def _dist(self, A, B):
    ax, ay = A
    bx, by = B
    return (ax - bx) * (ax - bx) + (ay - by) * (ay - by)
  
  def is_intersection(self, p0, p1, q0, q1):
    c0 = self._cross(p0, p1, q0)
    c1 = self._cross(p0, p1, q1)
    d0 = self._cross(q0, q1, p0)
    d1 = self._cross(q0, q1, p1)
    if c0 == c1 == 0:
      e0 = self._dot(p0, p1, q0)
      e1 = self._dot(p0, p1, q1)
      if not e0 < e1:
        e0, e1 = e1, e0
      return e0 <= self._dist(p0, p1) and 0 <= e1
    return c0 * c1 <= 0 and d0 * d1 <= 0


#######################

