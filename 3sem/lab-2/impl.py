import unittest
from functools import cache
import pandas as pd

import numpy
from numpy import sign
DEFAULT_EPS = 10**-3
GOLDEN = (1 + 5 ** 0.5) / 2
K = (3 - 5 ** 0.5) / 2

# -- Методы оптимизации --


def dichotomy(f, a, b, eps=DEFAULT_EPS):
    """Метод дихотомии"""
    list = []
    if a > b:
        a, b = b, a
    list.append([a, b])
    calls = 0
    while abs(b - a) > eps:
        delta = (b - a) / 4
        x_1 = (a + b) / 2 - delta
        x_2 = (a + b) / 2 + delta
        y_1 = f(x_1)
        y_2 = f(x_2)
        calls += 2
        if y_1 > y_2:
            a = x_1
        else:
            b = x_2
        list.append([round(a, 3), round(b, 3)])
    return (a + b) / 2, calls, round(calls/2), list
    # функция возвращает: найденное значение минимума, кол-во вызовов функции, итераций, массив измениний границ отрезка


def golden(f, a, b, eps=DEFAULT_EPS):
    """Метод золотого сечения"""
    list = []
    if a > b:
        a, b = b, a
    list.append([a, b])
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
        list.append([round(a, 3), round(b, 3)])
    return (a + b) / 2, calls, calls - 1, list


@cache
def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)


def fibonacci(f, a, b, eps=DEFAULT_EPS):
    """Метод Фибоначчи"""
    list = []
    if a > b:
        a, b = b, a
    list.append([a, b])
    n = 1
    while fib(n) <= (b - a) / eps:
        n += 1
    l = a + fib(n - 2) / fib(n) * (b - a)
    m = a + fib(n - 1) / fib(n) * (b - a)
    y_l = None
    y_m = None
    calls = 0
    iteration_counter = 0
    for k in range(2, n):
        calls += int(not y_l) + int(not y_m)
        iteration_counter+=1
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
        list.append([round(a, 3), round(b, 3)])
    m = l + eps
    y_m = None
    calls += int(not y_l) + int(not y_m)
    iteration_counter+=1
    y_l = y_l or f(l)
    y_m = y_m or f(m)
    if y_l > y_m:
        a = l
    else:
        b = l
    list.append([round(a, 3), round(b, 3)])
    return (a + b) / 2, calls, iteration_counter, list


def pauell(f, x_1, eps=DEFAULT_EPS):
    """Метод парабол"""
    h = eps
    x_v = None
    x_min = None
    y_min = None
    y_1 = None
    calls = 0
    iterations_counter = 0
    list = []
    while True:
        iterations_counter += 1
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
        list.append([round(x_1, 3), round(x_3, 3)])
        calls += 2
        x_min, y_min = min((x_1, y_1), (x_2, y_2),
                           (x_3, y_3), key=lambda p: p[1])
        x_v = (x_2 - x_1) / 2 - ((y_2 - y_1) / (x_2 - x_1)) / \
            (2 * (1 / (x_3 - x_2)) * ((y_3 - y_1) /
             (x_3 - x_1) - (y_2 - y_1) / (x_2 - x_1)))
        if abs(x_v - x_min) <= eps:
            break
    return x_v, calls, iterations_counter, list


def brent(f, a, b, eps=DEFAULT_EPS):
    list = [[a, b]]
    x = w = v = (a + b) / 2
    y_x = y_w = y_v = f(x)
    calls = 1
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
        calls += 1
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
        list.append([round(a, 3), round(b, 3)])
    return (a + b) / 2, calls, calls - 1, list

# -- Тестирование методов --

# Функции для тестирования


def quadraticFunction(x):
    return x**2


def functionFromVariant(x):
    return numpy.sin(x) * x**3

# Функции проверки
def checkValue(value, actualValue, eps=DEFAULT_EPS):
    errorString = f"Expected: {actualValue}\tGot: {value}\tEpsilon: {eps}"
    assert abs(actualValue - value) <= eps, errorString

def checkMethosds(f, a, b, actualValue, eps=DEFAULT_EPS):
    checkValue(dichotomy(f, a, b, eps)[0], actualValue)
    checkValue(golden(f, a, b, eps)[0], actualValue)
    checkValue(pauell(f, a, eps)[0], actualValue)
    checkValue(brent(f, a, b, eps)[0], actualValue)

def produceRowsForDifferentEps(list_eps, f, a, b):
    for i in range(len(list_eps)):
        yield(list_eps[i], dichotomy(f, a, b, list_eps[i])[2], dichotomy(f, a, b, list_eps[i])[1],
            golden(f, a, b, list_eps[i])[2], golden(f, a, b, list_eps[i])[1],
            fibonacci(f, a, b, list_eps[i])[2], fibonacci(f, a, b, list_eps[i])[1],
            pauell(f, a, list_eps[i])[2], pauell(f, a, list_eps[i])[1],
            brent(f, a, b, list_eps[i])[2], brent(f, a, b, list_eps[i])[1],)


def produceRowsOfBorders(f, a, b):
    dich_list = dichotomy(f, a, b, DEFAULT_EPS)[3]
    gold_list = golden(f, a, b, DEFAULT_EPS)[3]
    gold_list.extend('-' * 50)
    fib_list = fibonacci(f, a, b, DEFAULT_EPS)[3]
    fib_list.extend('-' * 50)
    pau_list = pauell(f, a, DEFAULT_EPS)[3]
    pau_list.extend('-' * 50)
    brent_list = brent(f, a, b, DEFAULT_EPS)[3]
    brent_list.extend('-' * 50)
    
    for i in range(len(dich_list)):
        yield(i,
            dich_list[i], 
            gold_list[i], 
            fib_list[i], 
            pau_list[i], 
            brent_list[i])
    

# Проверка


checkMethosds(quadraticFunction, -1, 1, 0)
checkMethosds(functionFromVariant, -2, 2, 0)
list_eps = [10**-2, 10**-3, 10**-4]
table = pd.DataFrame(produceRowsForDifferentEps(list_eps, functionFromVariant, -2, 2), 
                     columns=["eps", "dich_iter", "dich_calls", "gold_iter", "gold_calls",
                              "fib_iter", "fib_calls", "pau_iter", "pau_calls", "brent_iter", "brent_calls"])
with open('table.csv', 'w') as csvfile:
    table.style.hide(axis="index").format(
        precision=5).to_latex(buf=csvfile)
    
lists_of_borders = pd.DataFrame(produceRowsOfBorders(functionFromVariant, -2, 2), columns=["iter", "dich", "gold", "fib", "pau", "brent"])
with open('lists.csv', 'w') as csvfile:
    lists_of_borders.style.hide(axis="index").format(
        precision=5).to_latex(buf=csvfile)

