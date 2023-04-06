from functools import cache

import numpy
from numpy import sign
DEFAULT_EPS = 10**-4
GOLDEN = (1 + 5 ** 0.5) / 2
K = (3 - 5 ** 0.5) / 2

# -- Методы оптимизации --
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


def pauell(f, x_1, eps=DEFAULT_EPS):
    """Метод парабол"""
    h = 2 * eps
    x_v = None
    x_min = None
    y_min = None
    y_1 = None
    calls = 0
    while x_v and x_min and abs(x_v - x_min) > eps:
        if x_min and x_v:
            y_v = f(x_v)
            x_1, y_1 = (x_v, y_v) if y_v < y_min else (x_min, y_min)
            calls += 1

        x_2 = x_1 + h
        calls += int(not y_1)
        y_1 = y_1 or f(x_1)
        y_2 = f(x_2)
        x_3 = x_1 + 2 * h if y_1 > y_2 else x_1 - h
        y_3 = f(x_3)
        calls += 2
        x_min, y_min = min((x_1, y_1), (x_2, y_2),
                           (x_3, y_3), key=lambda p: p[1])
        x_v = (x_2 - x_1) / 2 - ((y_2 - y_1) / (x_2 - x_1)) / \
            (2 * (1 / (x_3 - x_2)) * ((y_3 - y_1) /
             (x_3 - x_1) - (y_2 - y_1) / (x_2 - x_1)))
    return x_v, calls


def brent(f, a, b, eps=DEFAULT_EPS):
    x = w = v = (a + b) / 2
    y_x = y_w = y_v = f(x)
    d = b - a
    u = 0
    while abs(b - a) > eps:
        g = d
        if abs(y_x - y_w) > eps and abs(y_x - y_v) and abs(y_w - y_v) > eps:
            u = w - ((w - x) ** 2 * (y_w - y_v) - (w - v) ** 2 * (y_w - y_x)) / \
                2 * ((w - x) * (y_w - y_v) - (w - v) * (y_w - y_x))
        if a + eps < u < b - eps and abs(u - x) < g / 2:
            d = abs(u - x)
        else:
            if x < (b - a) / 2:
                u = x + K * (b - x)
                d = b - x
            else:
                u = x - K * (x - a)
                d = x - a
        if abs(u - x) < eps:
            u = x + sign(u - x) * eps
        y_u = f(u)
        if y_u <= y_x:
            if u >= x:
                a = x
            else:
                b = x
            v = w = x = u
            y_v = y_w = y_x = y_u
        else:
            if u >= x:
                b = u
            else:
                a = u
            if y_u <= y_w or abs(w - x) < eps:
                v = w = u
                y_v = y_w = y_u
            elif y_u <= y_v or abs(v - x) < eps or abs(w - v) < eps:
                v = u
                y_v = y_u

# -- Тестирование методов --

# Функции для тестирования
def quadraticFunction(x):
    return x**2

def functionFromVariant(x):
    return numpy.sin(x) * x**2
