import matplotlib.pyplot as plt
import random

class KmeansPlusPlus:

  def __init__(self, k, max_iter=10):
    self._k = k
    self._max_iter = max_iter

  def dist(self, s, t):
    # 小さいほど同じグループの可能性が高い
    return (s[0]-t[0])**2 + (s[1]-t[1])**2

  def mean(self, L: list):
    # 代表値を求める
    # mid
    x = sorted(x for x,y in L)
    y = sorted(y for x,y in L)
    return [x[len(L)//2], y[len(L)//2]]
    # ave
    x, y = sum(x for x,y in L)//len(L), sum(y for x,y in L)//len(L)
    return [x, y]

  def fit(self, X):
    n = len(X)
    first_cluster = [X[random.randrange(0, n)]]
    cluster_set = set(first_cluster)

    while len(first_cluster) < self._k:
      p_f = [0 if x in cluster_set else min(self.dist(x, f) for f in first_cluster) for x in X]
      tmpk = random.choices(X, weights=p_f, k=1)[0]
      cluster_set.add(tmpk)
      first_cluster.append(tmpk)

    cluster_centers = first_cluster
    labels = [-1] * n
    for i in range(n):
      dist = self.dist(X[i], first_cluster[0])
      for j in range(self._k):
        tmp = self.dist(X[i], first_cluster[j])
        if tmp <= dist:
          dist = tmp
          labels[i] = j

    for _ in range(self._max_iter):
      syuukei = [[] for _ in range(self._k)]
      for i in range(n):
        syuukei[labels[i]].append(X[i])
      cluster_centers = [self.mean(syuukei[i]) for i in range(self._k)]
      for i in range(n):
        dist = self.dist(X[i], first_cluster[0])
        for j in range(self._k):
          tmp = self.dist(X[i], first_cluster[j])
          if tmp <= dist:
            dist = tmp
            labels[i] = j
    return labels, cluster_centers


if __name__ == '__main__':

  k = 9
  n = 10
  x, y = [], []
  for i in range(0, 900, 300):
    for j in range(0, 900, 300):
      x.extend([random.randrange(i+50, i+150) for _ in range(n)])
      y.extend([random.randrange(j+50, j+150) for _ in range(n)])
  n = len(x)
  model = KmeansPlusPlus(k, max_iter=10)
  data = [(x[i], y[i]) for i in range(n)]
  labels, cluster_centers = model.fit(data)

  fig, ax = plt.subplots()
  ax.scatter(x, y, linewidth=0, label='')
  ax.minorticks_on()
  ax.tick_params(which='both', top='on', right='on', direction='in')
  ax.grid(which='major', axis='both')
  ax.legend(loc='lower right')
  plt.show()
  fig, ax = plt.subplots()
  color = {0: 'black',
           1: 'green',
           2: 'orange',
           3: 'darkblue',
           4: 'gray',
           5: 'brown',
           6: 'cyan',
           7: 'yellow',
           8: 'lightblue',
           9: 'pink'}
  for i in range(n):
    ax.scatter(x[i], y[i], color=color[labels[i]])
  for x,y in cluster_centers:
    ax.scatter(x, y, color='red', linewidth=5)
  plt.show()
  # plt.savefig('a.png')
