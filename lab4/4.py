import matplotlib as plt

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
plt.plot(test_data, label='Исходный временной ряд')
plt.plot(np.arange(train_size + lag_order, len(t)), y_pred, label='Предсказанные значения', linestyle='--')
plt.xlabel('Момент времени $t$')
plt.ylabel('Значения ряда')
plt.legend()
plt.savefig('prediction_comparison.svg')