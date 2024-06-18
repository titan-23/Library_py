from decimal import Decimal, getcontext


def decimal_pi():
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


def decimal_exp(x):
    getcontext().prec += 2
    i, lasts, s, fact, num = 0, 0, 1, 1, 1
    while s != lasts:
        lasts = s
        i += 1
        fact *= i
        num *= x
        s += num / fact
    getcontext().prec -= 2
    return +s


def decimal_cos(x):
    getcontext().prec += 2
    i, lasts, s, fact, num, sign = 0, 0, 1, 1, 1, 1
    while s != lasts:
        lasts = s
        i += 2
        fact *= i * (i - 1)
        num *= x * x
        sign *= -1
        s += num / fact * sign
    getcontext().prec -= 2
    return +s


def decimal_sin(x):
    getcontext().prec += 2
    i, lasts, s, fact, num, sign = 1, 0, x, 1, x, 1
    while s != lasts:
        lasts = s
        i += 2
        fact *= i * (i - 1)
        num *= x * x
        sign *= -1
        s += num / fact * sign
    getcontext().prec -= 2
    return +s


def decimal_acos(x):
    if x < -1 or x > 1:
        raise ValueError("math domain error")
    if x == 1:
        return Decimal(0)
    if x == -1:
        return decimal_pi()
    epsilon = Decimal("1e-" + str(getcontext().prec))
    getcontext().prec += 2
    sum_acos = Decimal(0)
    term = x
    power = x**2
    n = 0
    while abs(term) > epsilon:
        n += 1
        term *= Decimal((2 * n - 1) * (2 * n)) / (4 * n * n * (2 * n + 1))
        term *= power
        sum_acos += term
        power *= x**2
    result = decimal_pi() / 2 - sum_acos
    getcontext().prec -= 2
    return +result
