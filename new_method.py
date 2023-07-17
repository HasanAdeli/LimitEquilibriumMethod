from model import cost
from pso_algorithm import Pso


# print(cost([-5.449153975197992]))
pso = Pso(0.7, 0.7, 1.4, 0.99, cost, 50, 5000, 1, 1, [-5], [5])
pso.run(constriction_coefficient=False)
