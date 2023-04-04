from functools import cache
DEFAULT_EPS = 10**-4
GOLDEN = (1 + 5 ** 0.5) / 2


def dichotomy(f, a, b, delta, eps=DEFAULT_EPS):
    """Метод дихотомии"""
    if a > b:
        a, b = b, a
    if not 0 < delta < (b-a)/2:
        raise ValueError("Delta must be in range (0, (b-a)/2)")
    calls = 0
    while abs(b - a) > eps:
        x_1 = (a + b) / 2 - delta
        x_2 = (a + b) / 2 + delta
        y_1 = f(x_1)
        y_2 = f(x_2)
        calls += 2
        if y_1 > y_2:
            a = x_1
            y_1 = None
        else:
            b = x_2
            y_2 = None
    return (a + b) / 2, calls


def golden(f, a, b, eps=DEFAULT_EPS):
    """Метод золотого сечения"""
    if a > b:
        a, b = b, a
    calls = 0
    y_1 = None
    y_2 = None
    while abs(b - a) > eps:
        t = (b - a) / GOLDEN
        x_1 = b - t
        x_2 = a + t
        calls += int(not y_1) + int(not y_2)
        y_1 = y_1 or f(x_1)
        y_2 = y_2 or f(x_2)
        if y_1 > y_2:
            a = x_1
            y_1 = y_2
            y_2 = None
        else:
            b = x_2
            y_2 = y_1
            y_1 = None
    return (a + b) / 2, calls


@cache
def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)


def fibonacci(f, a, b, eps=DEFAULT_EPS):
    """Метод Фибоначчи"""
    if a > b:
        a, b = b, a
    n = 1
    while fib(n) <= (b - a) / eps:
        n += 1
    l = a + fib(n - 2) / fib(n) * (b - a)
    m = a + fib(n - 1) / fib(n) * (b - a)
    y_l = None
    y_m = None
    calls = 0
    for k in range(1, n - 2):
        calls += int(not y_l) + int(not y_m)
        y_l = y_l or f(l)
        y_m = y_m or f(m)
        if y_l > y_m:
            a = l
            l = m
            m = a + fib(n - k - 1) / fib(n - k) * (b - a)
            y_m = None
        else:
            b = m
            m = l
            l = a + fib(n - k - 2) / fib(n - k) * (b - a)
            y_l = None
        m = l + eps
    calls += int(not y_l) + int(not y_m)
    y_l = y_l or f(l)
    y_m = y_m or f(m)
    if abs(y_l - y_m) < eps:
        a = l
    elif y_l < y_m:
        b = m
    return (a + b) / 2, calls

# TODO: Pauell's and Brent's methods (метод парабол и Брента)
