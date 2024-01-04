
# from typing import Generic, Tuple, TypeVar, List
# T = TypeVar('T')

# class RadixHeapArray(Generic[T]):

#   def __init__(self, u: int, n: int):
#     self.u = u
#     self.log = u.bit_length()
#     self.lim = (1 << self.log) - 1
#     self.last = 0
#     self._len = 0
#     self.data: List[List[Tuple[int, T]]] = [[] for _ in range(self.log)]

#     # key, i(in data[x])
#     self.rev = [(-1, -1) for _ in range(n)]
#     self.n = n

#   def set_key(self, key: int, i: int) -> None:
#     old_key, indx = self.rev[i]
#     if indx == -1:
#       self.push(key, i)
#       return
#     old_x = (old_key ^ self.last).bit_length()
#     old_key, _ = self.data[old_x][indx]
#     back_key, back_i = self.data[old_x].pop()
#     if indx != len(self.data[old_x]):
#       self.data[old_x][indx] = (back_key, back_i)
#       self.rev[back_i] = (back_key, indx)
#     new_x = (key ^ self.last).bit_length()
#     self.rev[i] = (key, len(self.data[new_x]))
#     self.data[new_x].append((key, i))

#   def __setitem__(self, k: int, v: int):
#     self.set_key(v, k)

#   def push(self, key: int, i: int) -> None:
#     assert key <= self.lim
#     self._len += 1
#     x = (key ^ self.last).bit_length()
#     self.rev[i] = (key, len(self.data[x]))
#     self.data[x].append((key, i))

#   def top(self) -> Tuple[int, T]:
#     data = self.data
#     if not data[0]:
#       for d in data:
#         if not d: continue
#         return min(d)
#     return data[0][-1]

#   def pop(self) -> Tuple[int, T]:
#     assert len(self) == sum(len(x) for x in self.data)
#     self._len -= 1
#     data, rev = self.data, self.rev
#     if not data[0]:
#       for d in data:
#         if not d: continue
#         last = min(d)[0]
#         for key, i in d:
#           x = (key ^ last).bit_length()
#           rev[i] = (key, len(data[x]))
#           data[x].append((key, i))
#         d.clear()
#         self.last = last
#         break
#     key, i = data[0].pop()
#     rev[i] = (-1, -1)
#     return (key, i)

#   def __len__(self):
#     return self._len

#   def __bool__(self):
#     return self._len > 0

#   def __str__(self):
#     a = []
#     for d in self.data:
#       a.extend(d)
#     return str(a)

