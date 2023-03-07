# --------------------------------------------
# Oбязательные входные данные

# (левая граница, правая граница, шаг)
a, b, h = map(float, input().split())

# сама функция
def Function(x):
    # здесь должно возвращаться значение функции
    return x

# --------------------------------------------
# Далее все вычисления

# шаг сетки
n = (a-b)/h;

# значения x от i
def getXOnIteration (i):
    if i < 0 or type(i) is int:
        raise ValueError("Value (i) mast be natural number");
    return a + h*i

#--Производные--

# нахождение правой разностной производной в точке
def rightDifferenceDerivative(x, func):
    return (func(x+h)-func(x))/h

# находение левой разностной производной в точке
def leftDifferenceDerivative(x, func):
    return (func(x)-func(x-h))/h

# более точная производная в точке при задействии трёх узлов
def derivativeWithIncreasedPrecision(i, func):
    return (func(getXOnIteration(i + 1)) - func(getXOnIteration(i - 1)))/(2 * h)

# производные в граничных точках
def leftExtremeDerivative(func):
    return (-3 * func(getXOnIteration(0)) + 4 * func(getXOnIteration(1)) - func(getXOnIteration(2)))/(2 * h)

def rightExtremeDerivative(func):
    return (func(getXOnIteration(n - 2)) - 4 * func(getXOnIteration(n - 1)) + 3 * func(getXOnIteration(n)))/(2 * h)

#--Интегралы--
