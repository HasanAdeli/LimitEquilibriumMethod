import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt

from model import CoastFunction
from pso_algorithm import Pso


problem_data = {
    'height': 12,
    'slope': 1/2.6,
    'water_height_left': 10,
    'water_height_right': 4
}


def optimum_slip_surface(data):
    static_data = [data['height'], data['slope'], data['water_height_left'], data['water_height_right']]
    pso = Pso(0.9, 0.9, 1.4, 0.99, objective_function, static_data, 40, 100, 4, 4, [7, 10, 20, -10], [12, 15, 30, 10])
    pso.run(constriction_coefficient=True)
    x, y, r, theta = pso.best_pos[-1]
    print("*" * 150)
    print('∑𝑄𝑖 + ∑𝑀𝑖: ', pso.best_costs[-1])
    print("x center circle: ", x)
    print("y center circle: ", y)
    print("radius: ", r)


def objective_function_(x0, data, static_data):
    print('fs: ', x0)
    x, y, r, theta = data
    c = CoastFunction()
    q, qb = c.cost(x, y, r, theta, [x0] + static_data)
    print('cost: ', abs(q + qb))
    print('-'*200)
    return abs(q + qb)


def objective_function(x0, data, static_data):
    x, y, r = data
    theta = x0[1]
    c = CoastFunction()
    q, qb = c.cost(x, y, r, theta, [x0[0]] + static_data)
    cost = abs(q + qb)
    return


def cost_calc(fs, data, static_data):
    x, y, r, theta = data
    c = CoastFunction()
    q, qb = c.cost(x, y, r, theta, [fs] + static_data)
    return abs(q + qb)


def rosen(x):

    """The Rosenbrock function"""
    result = sum(100.0*(x[1:]-x[:-1]**2.0)**2.0 + (1-x[:-1])**2.0)

    return result


def example(x):
    print(x)
    result = (x - 2) * (x + 1) ** 2
    return result


height, slope, water_height_left, water_height_right = 12, 1/2.6, 10, 4
static_data = [height, slope, water_height_left, water_height_right]
data = 8, 13, 25  # x, y, r, t

# res = minimize(
#     rosen,
#     x0=np.array([1.3, 0.7, 0.8, 1.9, 1.2]),
#     # args=(data, static_data),
#     method='nelder-mead',
#     options={'xatol': 1e-8, 'disp': True}
# )

# res = minimize_scalar(objective_function_, args=(data, static_data), bounds=(0.1, 20), method='bounded')
res = minimize(objective_function, x0=np.array([1.3, 2.0]), args=(data, static_data), method='Powell')

print(res)
print(res.x)
