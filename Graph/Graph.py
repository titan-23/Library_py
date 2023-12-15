from Library_py.DataStructures.Array.CSRArray import CSRArray

class Graph():

  def __init__(self, n: int) -> None:
    self.G = [[] for _ in range(n)]

  def add_edge(self, u: int, v: int) -> None:
    self.G[u].append(v)

  def build_csr(self) -> None:
    self.csr = CSRArray(self.G)


