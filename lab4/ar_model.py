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
