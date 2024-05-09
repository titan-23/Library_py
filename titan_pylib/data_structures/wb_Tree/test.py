v = 1
D = 3
G = 2


def is_balance(l, r):
    if l < 0 or r < 0:
        return False
    return (l + 1) * D >= (r + 1) and (r + 1) * D >= (l + 1)


def gen_lr(v):
    for l in range(v + 1):
        r = v - l - 1
        if is_balance(l, r):
            yield l, r


check = 0
MAX = 50
for l in range(MAX):
    for r in range(MAX):
        if is_balance(l, r):
            continue
        if (l + 1) * D >= (r + 1):
            continue
        # rが大きい場合
        for a, b in gen_lr(r):
            assert a + b + 1 == r
            assert is_balance(a, b)
            x = l + v + a
            if is_balance(x, b):
                # ok.
                continue
            if (x + 1) * D < (b + 1):
                # bがでかいとき
                assert False
            # 常にxがでかいらしい
            assert (b + 1) * D < (x + 1)
            for sl, sr in gen_lr(x):
                for t, u in gen_lr(sr):
                    assert is_balance(t, u)
                    # print(f"{check=}")
                    check += 1
                    if (sr + 1) >= (sl + 1) * G:
                        # double
                        assert is_balance(sl, t)
                        assert is_balance(u, b)
                        assert is_balance(sl + t + 1, u + b + 1)
                    else:
                        # single
                        assert is_balance(sr, b)
                        assert is_balance(sl, sr + b + 1)
print("ok")
