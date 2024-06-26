# 展開に失敗しました
from decimal import Decimal, getcontext
import math


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


def decimal_cos(x: Decimal) -> Decimal:
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


def decimal_sin(x: Decimal) -> Decimal:
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


def decimal_asin(x: Decimal) -> Decimal:
    assert isinstance(x, Decimal)
    if x < -1 or x > 1:
        raise ValueError("math domain error")
    if x == 1:
        return decimal_pi() / 2
    if x == -1:
        return -decimal_pi() / 2
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
    result = sum_acos
    getcontext().prec -= 2
    return +result


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
