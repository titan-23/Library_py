sys.setrecursionlimit(10**6)
# https://gist.github.com/tjkendev/231897301fde67d4a81f51c3f0873936

# Chu-Liu/Edmonds' Algorithm
# 最小全域有向木を再帰的に求める
# V: 頂点数, es: 辺集合, r: 根となる頂点番号
def Minimum_Cost_Arborescence(V, es, r):
  # まず、頂点vに入るものの内、コストが最小の辺を選択する
  # minsには(最小コスト, その辺のもう一方の頂点番号)
  mins = [(10**18, -1)]*V
  for s, t, w in es:
    mins[t] = min(mins[t], (w, s))
  # 根となる頂点rからは何も選択しない
  mins[r] = (-1, -1)

  group = [0]*V # 縮約した際に割り振られる頂点番号
  comp = [0]*V  # 縮約されたgroupか
  cnt = 0       # 縮約した後の頂点数

  # 縮約処理
  used = [0]*V
  for v in range(V):
    if not used[v]:
      chain = [] # 探索時に通った頂点番号リスト
      cur = v    # 現在探索中の頂点
      while not used[cur] and cur!=-1:
        chain.append(cur)
        used[cur] = 1
        cur = mins[cur][1]
      if cur!=-1:
        # 探索が根の頂点rで終了しなかった場合
        # chain = [a0, a1, ..., a(i-1), ai, ..., aj], cur = aiの場合
        # a0, ..., a(i-1)までは固有の番号を割り振り
        # ai, ..., ajまでは閉路であるため、同じ番号を割り振るようにする
        cycle = 0
        for e in chain:
          group[e] = cnt
          if e==cur:
            # 閉路を見つけた
            cycle = 1
            comp[cnt] = 1
          if not cycle:
            cnt += 1
        if cycle:
          cnt += 1
      else:
        # 探索が根の頂点rで終了した場合
        # --> 閉路を持たないため、１つずつ新しい番号を割り振っていく
        for e in chain:
          group[e] = cnt
          cnt += 1

  # cntがV => 閉路が存在せず、有向木が構築できている
  if cnt == V:
    # 根の頂点r以外が選択した辺のコストの和を返す
    # (+1はmins[r][0]の-1を打ち消すやつ)
    return sum(map(lambda x:x[0], mins)) + 1

  # 閉路が含まれていた場合
  # --> 閉路に含まれている頂点が選択した辺のコストの和を計算
  res = sum(mins[v][0] for v in range(V) if v!=r and comp[group[v]])

  # 再帰的に計算するグラフが持つ辺を構築
  n_es = []
  for s, t, w in es:
    # 追加する辺に繋がる頂点は、新しいグラフの頂点番号に変換する
    gs = group[s]; gt = group[t]
    if gs == gt:
      # 同じ閉路に含まれている頂点どうしをつなぐ辺の場合
      # --> 追加しない
      continue
    if comp[gt]:
      # ある閉路に含まれている頂点vに入る辺の場合
      # --> その辺のコストから、閉路においてその頂点vに入っていた辺のコストを引く
      n_es.append((gs, gt, w - mins[t][0]))
    else:
      # その他 --> 何もせず追加
      n_es.append((gs, gt, w))

  # 再帰的に求めた最小コストと、さっき計算したコストresを足したものを返す
  return res + Minimum_Cost_Arborescence(cnt, n_es, group[r])
