from decimal import Decimal, getcontext


def decimal_pi() -> Decimal:
    getcontext().prec += 2
    three = Decimal(3)
    lasts, t, s, n, na, d, da = 0, three, 3, 1, 0, 0, 24
    while s != lasts:
        lasts = s
        n, na = n + na, na + 8
        d, da = d + da, da + 32
        t = (t * n) / d
        s += t
    getcontext().prec -= 2
    return +s


def decimal_exp(x: Decimal) -> Decimal:
    getcontext().prec += 5
    eps = Decimal("1e-" + str(getcontext().prec))
    term = Decimal(1)
    sum_exp = term
    n = 1
    while abs(term) > eps:
        term *= x / n
        sum_exp += term
        n += 1
    getcontext().prec -= 5
    return +sum_exp


def decimal_cos(x: Decimal) -> Decimal:
    getcontext().prec += 5
    eps = Decimal("1e-" + str(getcontext().prec))
    term = Decimal(1)
    sum_cos = term
    x2 = x * x
    n = 1
    while abs(term) > eps:
        term *= -x2 / (2 * n * (2 * n - 1))
        sum_cos += term
        n += 1
    getcontext().prec -= 5
    return +sum_cos


def decimal_sin(x: Decimal) -> Decimal:
    getcontext().prec += 5
    eps = Decimal("1e-" + str(getcontext().prec))
    term = x
    sum_sin = term
    x2 = x * x
    n = 1
    while abs(term) > eps:
        term *= -x2 / (2 * n * (2 * n + 1))
        sum_sin += term
        n += 1
    getcontext().prec -= 5
    return +sum_sin


def decimal_asin(x: Decimal) -> Decimal:
    assert isinstance(x, Decimal)
    getcontext().prec += 5
    eps = Decimal("1e-" + str(getcontext().prec))
    if x < -1 or x > 1:
        getcontext().prec -= 5
        raise ValueError("math domain error")
    if x > Decimal(1) - eps:
        getcontext().prec -= 5
        return decimal_pi() / 2
    if x < Decimal(-1) + eps:
        getcontext().prec -= 5
        return -decimal_pi() / 2
    if abs(x) < Decimal("0.5"):
        y = x + x**3 / 6
    else:
        y = Decimal("0.5") * (decimal_pi() / 2 - x)
    while True:  # ニュートン法で収束を高速化
        y_new = y - (decimal_sin(y) - x) / (
            Decimal(1) - decimal_sin(y + eps) + decimal_sin(y)
        )
        if abs(y_new - y) < eps:
            break
        y = y_new
    getcontext().prec -= 5
    return +y


def decimal_acos(x: Decimal) -> Decimal:
    assert isinstance(x, Decimal)
    if x < -1 or x > 1:
        raise ValueError("math domain error")
    if x == 1:
        return Decimal(0)
    if x == -1:
        return decimal_pi()
    getcontext().prec += 2
    eps = Decimal("1e-" + str(getcontext().prec))
    sum_acos = x
    term = Decimal(1)
    power = x
    n = 0
    while abs(term * power) > eps:
        n += 1
        term *= (2 * n - 1) * (2 * n) * (2 * (n - 1) + 1)
        term /= 4 * n * n * (2 * n + 1)
        power *= x * x
        sum_acos += term * power
    result = decimal_pi() / 2 - sum_acos
    getcontext().prec -= 2
    return +result


def decimal_atan(x: Decimal) -> Decimal:
    return decimal_asin(x / (1 + x * x).sqrt())
