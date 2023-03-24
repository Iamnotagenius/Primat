# -------------------------------------------
# Oбязательные входные данные

from statistics import pvariance
from math import sqrt, exp
import pandas as pd

a = 0
"""Левая граница"""

b = 1
"""Правая граница"""

h = 0.1
"""Шаг"""


def func(x: float):
    return exp(x)


def derivative(x: float):
    return exp(x)

# --------------------------------------------
# Далее все инструменты для вычисления


n = round((b - a) / h)
"""Шаг сетки"""


def getXOnIteration(i: float):
    """Значения x от i"""
    if i < 0:
        raise ValueError("Value (i) mast be more 0")
    return a + h * i

# --Производные--


def rightDifferenceDerivative(x):
    """Нахождение правой разностной производной в точке"""
    return (func(x + h) - func(x)) / h


def leftDifferenceDerivative(x):
    """Находение левой разностной производной в точке"""
    return (func(x) - func(x - h)) / h


def derivativeWithIncreasedPrecision(i):
    """Более точная производная в точке при задействии трёх узлов"""
    return (func(getXOnIteration(i + 1)) - func(getXOnIteration(i - 1))) / (2 * h)


def leftExtremeDerivative():
    """Производная в левой граничной точке"""
    return (-3 * func(getXOnIteration(0)) + 4 * func(getXOnIteration(1)) - func(getXOnIteration(2))) / (2 * h)


def rightExtremeDerivative():
    """Производная в правой граничной точке"""
    return (func(getXOnIteration(n - 2)) - 4 * func(getXOnIteration(n - 1)) + 3 * func(getXOnIteration(n))) / (2 * h)

# --Элементарные интегралы--
# У всех должен быть только один входной парамер (i)


def leftElementaryIntegral(i):
    """Метод левых прямоугольников"""
    return h * func(getXOnIteration(i - 1))


def rightElementaryIntegral(i):
    """Метод правых прямоугольников"""
    return h * func(getXOnIteration(i))


def centralElementaryIntegral(i):
    """Метод центральных прямоугольников"""
    return h * func(getXOnIteration(i - 0.5))


def trapezoidElementaryIntegral(i):
    """Формула трапеции"""
    return (h / 2) * (func(getXOnIteration(i - 1)) + func(getXOnIteration(i)))


def simpsonElementaryIntegral(i):
    """Формула Симпсона"""
    return (h / 6) * (func(getXOnIteration(i)) + 4 * func(getXOnIteration(i - 0.5)) + func(getXOnIteration(i)))

# --Интегралы--


def integral(elementaryIntegral):
    """Находение интеграла через сумму элементарных интегралов"""
    sum = 0
    for i in range(1, n + 1):
        sum += elementaryIntegral(i)
    return sum

# --------------------------------------------
# Тут должны быть сами вычисления


def produce_rows():
    yield (getXOnIteration(0),
           leftDifferenceDerivative(a),
           rightDifferenceDerivative(a),
           leftExtremeDerivative(),
           derivative(a)
           )
    for i in range(1, n):
        yield (getXOnIteration(i),
               leftDifferenceDerivative(getXOnIteration(i)),
               rightDifferenceDerivative(getXOnIteration(i)),
               derivativeWithIncreasedPrecision(i),
               derivative(getXOnIteration(i))
               )
    yield (getXOnIteration(n),
           leftDifferenceDerivative(b),
           rightDifferenceDerivative(b),
           rightExtremeDerivative(),
           derivative(b)
           )


df = pd.DataFrame(produce_rows(), columns=["x", "ldd", "rdd", "dwi", "dx"])
df["sd"] = df.apply(lambda s: sqrt(pvariance(s[1:4], s[4])), axis=1)
print(df)
with open('derivatives.csv', 'w') as csvfile:
    df.style.hide(axis="index").format(
        precision=5).to_latex(buf=csvfile)

for _ in range(5):
    df = pd.DataFrame(produce_rows(), columns=["x", "ldd", "rdd", "dwi", "dx"])
    df["sd"] = df.apply(lambda s: sqrt(pvariance(s[1:4], s[4])), axis=1)
    print(n, df["sd"].mean())
    h /= 2
    n = round((b - a) / h)
