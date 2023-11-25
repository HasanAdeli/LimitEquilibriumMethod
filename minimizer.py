import numpy as np
from scipy.optimize import minimize

from model import CoastFunction
from pso_algorithm import Pso


def optimum_slip_surface(data):
    static_data = [data['height'], data['slope'], data['water_height_left'], data['water_height_right']]
    pso = Pso(0.9, 0.9, 1.4, 0.99, get_cost, static_data, 50, 5, 3, 3, [8, 10, 20], [12, 15, 30])
    pso.run(constriction_coefficient=True)
    print('fs: ', pso.best_costs[-1])
    x, y, r = pso.best_pos[-1]
    print("x center circle: ", x)
    print("y center circle: ", y)
    print("radius: ", r)
    return x, y, r


def objective_function(x0, data, static_data):
    x, y, r = data
    theta = x0[1]
    c = CoastFunction()
    q, qb = c.cost(x, y, r, theta, [x0[0]] + static_data)
    return abs(q + qb)


def get_cost(data, static_data):
    res = minimize(objective_function, x0=np.array([1.3, 2.0]), args=(data, static_data), method='Powell')
    if res.x[0] < 1.3:
        return 10000
    return res.x[0]


if __name__ == '__main__':
    problem_data = {
        'height': 12,
        'slope': 1 / 2.6,
        'water_height_left': 10,
        'water_height_right': 4
    }

    result = optimum_slip_surface(problem_data)
    # static_data = [problem_data['height'], problem_data['slope'], problem_data['water_height_left'], problem_data['water_height_right']]
    # get_cost((x, y, r), static_data=static_data)
