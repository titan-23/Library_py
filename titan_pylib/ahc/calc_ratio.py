pre = "./alltests/2024-10-06_14-03-10/result.csv"
now = "./alltests/2024-10-06_14-03-36/result.csv"

predata = {}
nowdata = {}
with open(pre, "r", encoding="utf-8") as f:
    for line in f:
        filename, score = line.split()
        score = float(score)
        predata[filename] = score
with open(now, "r", encoding="utf-8") as f:
    for line in f:
        filename, score = line.split()
        score = float(score)
        nowdata[filename] = score

assert list(predata.keys()) == list(nowdata.keys())

filenames = sorted(set(predata.keys()) | set(nowdata.keys()))
res = 0
cnt = 0
for filename in filenames:
    res += nowdata[filename] / predata[filename]
    cnt += 1
    print(f"{filename} : {predata[filename]} -> {nowdata[filename]}")
print(f"ratio : {res / cnt}")
