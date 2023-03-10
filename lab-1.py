# -------------------------------------------
# Oбязательные входные данные

a = -1
"""Левая граница"""

b = 1
"""Правая граница"""

h = 0.01
"""Шаг"""


def func(x: float):
    """Функция для оптимизации"""
    return x ** 2

# --------------------------------------------
# Далее все инструменты для вычисления


n = round((a - b) / h)
"""Шаг сетки"""

# Значения x от i


def getXOnIteration(i: int):
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


print(integral(trapezoidElementaryIntegral))
