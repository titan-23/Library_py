#########################
#################
def grid_bfs(field, sx, sy, tx, ty, ng='#'):
  dx = [0, 1, 0, -1]
  dy = [1, 0, -1, 0]
  #     ↓ → ↑ ←
  n = len(field)
  m = len(field[0])
  dist = [[-1]*m for _ in range(n)]
  dist[sy][sx] = 0
  todo = deque([(sy, sx)])
  while todo:
    vy, vx = todo.popleft()
    for d in range(len(dx)):
      ny, nx = vy+dy[d], vx+dx[d]
      if 0 <= ny < n and 0 <= nx < m:
        if field[ny][nx] == ng or dist[ny][nx] != -1:
          continue
        dist[ny][nx] = dist[vy][vx] + 1
        if ny == ty and nx == tx:
          break
        todo.append((ny, nx))
    else:
      continue
    break
  # return dist

  direct = ('U', 'L', 'D', 'R')
  fukugen = []
  di = dist[ty][tx]
  gy, gx = ty, tx
  while di:
    for d in range(len(dx)):
      ny, nx = gy+dy[d], gx+dx[d]
      if 0 <= ny < n and 0 <= nx < m:
        if dist[ny][nx] == di - 1:
          di -= 1
          fukugen.append(direct[d])
          if ny == sy and nx == sx:
            break
          gy, gx = ny, nx
          break
  return fukugen[::-1]
