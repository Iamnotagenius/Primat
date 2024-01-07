import os
import numpy as np
import matplotlib.pyplot as plt

rnjesus = np.random.default_rng()
EPS = 1e-9

def is_stationary(a: np.ndarray):
    # characteristic polynomial is (-a_3 * x^3) + (-a_2 * x^2) + (-a_1 * x) + 1
    abs_roots = np.abs(np.roots(np.hstack((-a[:-1], np.ones(1)))))
    return np.all(abs_roots > 1)

def gen_from_ar_model(a: np.ndarray, x: np.ndarray, n=1, noise_scale=EPS):
    for _ in range(n):
        x = np.append(x, 0)
        x[-1] = np.sum(a * x[-4:] + rnjesus.normal(0, noise_scale, 4))
    return x

a = np.hstack((rnjesus.uniform(-1, 1, 3), rnjesus.uniform(-10, 10, 1))) 
while not is_stationary(a) or np.abs(a[0]) < EPS:
    a = rnjesus.uniform(-1, 1, 4)

assert is_stationary(a) and np.abs(a[0]) > EPS

ar_proc_str = f"x_t = {a[-1]:.3f} " + " ".join(f"+ {c:.3f}x_{{t-{i}}}" if c > 0 else f"- {-c:.3f}x_{{t-{i}}}" for i, c in enumerate(a[2::-1], 1))

print(f"Сгенерированный ряд:", ar_proc_str)
with open('ar_proc.tex', 'w') as f:
    f.write(ar_proc_str)
t = rnjesus.uniform(-10, 10, 3)
first_members_str = ", ".join(f"t_{i} = {x:.3f}" for i, x in enumerate(t))
print(f"Первые три значения рада:", first_members_str)
with open('first_members.tex', 'w') as f:
    f.write(first_members_str)

print("Генерируем ряд с дисперсией шума равной 0.1")

t = gen_from_ar_model(a, t, 1000, 0.1)

plt.figure()
plt.xlabel("Момент времени $t$")
plt.ylabel("Значения ряда")
plt.plot(t)
plt.savefig('process.svg')

# Задания 5,6

from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# Преобразование временного ряда в последовательность векторов задержек
def create_lagged_vectors(data, lag_order):
    X, y = [], []
    for i in range(len(data) - lag_order):
        X.append(data[i:i+lag_order])
        y.append(data[i+lag_order])
    return np.array(X), np.array(y)

# Разделение данных на обучающую и тестовую выборки
train_size = int(len(t) * 0.8)
train_data, test_data = t[:train_size], t[train_size:]

# Задайте порядок лага (в данном случае, 3)
lag_order = 3

# Создание обучающей и тестовой выборок в виде векторов задержек
X_train, y_train = create_lagged_vectors(train_data, lag_order)
X_test, y_test = create_lagged_vectors(test_data, lag_order)

# Инициализация и обучение модели машины опорных векторов
svr_model = SVR(kernel='linear')
svr_model.fit(X_train, y_train)

# Предсказание на тестовой выборке
y_pred = svr_model.predict(X_test)

# Оценка качества модели
mse = mean_squared_error(y_test, y_pred)
print(f'Mean Squared Error: {mse}')

# Вывод авторегрессионных параметров
ar_params = svr_model.coef_
print(f'Определенные авторегрессионные параметры: {ar_params}')

# Постройте график сравнения исходного временного ряда и предсказанных значений
plt.figure()
plt.plot(np.arange(len(train_data)), train_data, label='Исходный временной ряд (обучающая часть)')
plt.plot(np.arange(len(train_data), len(train_data) + len(X_test)), y_pred, label='Предсказанные значения (тестовая часть)')
plt.xlabel('Момент времени $t$')
plt.ylabel('Значения ряда')
plt.legend()
plt.savefig('prediction_comparison_fixed.svg')


# Эксперимент с различными ядрами и гиперпараметрами (7 задание)
kernels = ['linear', 'rbf', 'poly']
C_values = [0.1, 1, 10]
degree_values = [2, 3, 4]

best_mse = float('inf')
best_params = {}

for kernel in kernels:
    for C in C_values:
        for degree in degree_values if kernel == 'poly' else [None]:
            # Инициализация модели с текущими гиперпараметрами
            if kernel == 'poly':
                svr_model = SVR(kernel=kernel, C=C, degree=degree)
            else:
                svr_model = SVR(kernel=kernel, C=C)

            # Обучение модели
            svr_model.fit(X_train, y_train)

            # Предсказание на тестовой выборке
            y_pred = svr_model.predict(X_test)

            # Оценка качества модели
            mse = mean_squared_error(y_test, y_pred)

            # Сохранение наилучших параметров
            if mse < best_mse:
                best_mse = mse
                best_params = {'kernel': kernel, 'C': C, 'degree': degree}

print(f'Наилучшие параметры: {best_params}')
print(f'Mean Squared Error для наилучших параметров: {best_mse}')