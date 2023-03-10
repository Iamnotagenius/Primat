# -------------------------------------------
# Oбязательные входные данные

# (левая граница, правая граница, шаг)
a = -1
b = 1
h = 0.01

# Сама функция


def func(x: float):
    return x ** 2

# --------------------------------------------
# Далее все инструменты для вычисления


# Шаг сетки
n = round((a - b) / h)

# Значения x от i


def getXOnIteration(i: int):
    if i < 0:
        raise ValueError("Value (i) mast be more 0")
    return a + h * i

# --Производные--

# Нахождение правой разностной производной в точке


def rightDifferenceDerivative(x):
    return (func(x + h) - func(x)) / h

# Находение левой разностной производной в точке


def leftDifferenceDerivative(x):
    return (func(x) - func(x - h)) / h

# Более точная производная в точке при задействии трёх узлов


def derivativeWithIncreasedPrecision(i):
    return (func(getXOnIteration(i + 1)) - func(getXOnIteration(i - 1))) / (2 * h)

# Производные в граничных точках


def leftExtremeDerivative():
    return (-3 * func(getXOnIteration(0)) + 4 * func(getXOnIteration(1)) - func(getXOnIteration(2))) / (2 * h)


def rightExtremeDerivative():
    return (func(getXOnIteration(n - 2)) - 4 * func(getXOnIteration(n - 1)) + 3 * func(getXOnIteration(n))) / (2 * h)

# --Элементарные интегралы--
# У всех должен быть только один входной парамер (i)

# Метод левых прямоугольников


def leftElementaryIntegral(i):
    return h * func(getXOnIteration(i - 1))

# Метод правых прямоугольников


def rightElementaryIntegral(i):
    return h * func(getXOnIteration(i))

# Метод центральных прямоугольников


def centralElementaryIntegral(i):
    return h * func(getXOnIteration(i - 0.5))

# Формула трапеции


def trapezoidElementaryIntegral(i):
    return (h / 2) * (func(getXOnIteration(i - 1)) + func(getXOnIteration(i)))

# Формула симпсона


def simpsonElementaryIntegral(i):
    return (h / 6) * (func(getXOnIteration(i)) + 4 * func(getXOnIteration(i - 0.5)) + func(getXOnIteration(i)))

# --Интегралы--

# Этот интеграл находится через сумму элементарных интегралов


def integral(elementaryIntegral):
    sum = 0
    for i in range(1, n + 1):
        sum += elementaryIntegral(i)
    return sum

# --------------------------------------------
# Тут должны быть сами вычисления


print(integral(trapezoidElementaryIntegral))
