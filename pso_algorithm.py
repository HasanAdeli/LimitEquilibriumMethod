import time
import random
from math import sqrt
import numpy as np
import matplotlib.pyplot as plt

from shapes import Plot


class Pso:

    def __init__(self, c1, c2, w, w_damp, func, func_data, n_pop, max_iter, n_var, var_size, var_min, var_max):

        # --------------- PSO Parameter ------------------- #

        self.c1 = c1                 # personal learning coefficient
        self.c2 = c2                 # global learning coefficient
        self.w = w                   # inertia weight
        self.w_damp = w_damp         # inertia weight damping ratio
        self.n_pop = n_pop           # population size (swarm size)
        self.max_iter = max_iter     # maximum number of iteration

        # --------------- problem definition --------------- #

        self.func = func             # cost function
        self.func_data = func_data   # cost function static data
        self.n_var = n_var           # number of decision variables
        self.var_size = var_size     # size of decision variables matrix
        self.var_min = var_min       # lower bound of variables
        self.var_max = var_max       # upper bound of variables

        # --------------- Velocity limits ------------------ #

        # self.vel_max = 0.001 * (self.var_max[-1] - self.var_min[-1])
        self.vel_max = 0.01 * abs(self.var_min[0] - self.var_max[0])
        self.vel_min = -self.vel_max

        # --------------- initialization  ------------------ #
        self.particles = []
        self.best_costs = []
        self.best_pos = []
        self.global_best_cost = np.inf
        self.global_best_position = -np.inf

    def constriction_coefficient(self):
        phi1 = phi2 = 2.05
        phi = phi1 + phi2
        chi = 2 / (phi - 2 + sqrt((phi ** 2) - 4 * phi))
        self.w = chi
        self.c1 = self.c2 = chi * phi1

    def initialization(self):
        t1 = time.time()

        child_number = 0
        while len(self.particles) < self.n_pop:

            particle = Particle()

            # initialize position

            particle.position = [random.uniform(self.var_min[i], self.var_max[i]) for i in range(self.n_var)]

            # initialize velocity
            particle.velocity = [0 for _ in range(self.var_size)]

            # update particle cost function
            particle.cost = self.func(particle.position, self.func_data)

            # update personal best
            particle.best_position = particle.position
            particle.best_cost = particle.cost

            # create particle i-th
            self.particles.append(particle)
            print(f"child {child_number + 1} added")
            print(f"new child position: ", particle.position)
            print(f"new child cost: ", particle.cost)
            child_number += 1

            # update global best
            if particle.best_cost < self.global_best_cost:
                self.global_best_cost = particle.best_cost
                self.global_best_position = particle.best_position

        # print("********** result of particle generation **********")
        print("global best cost", self.global_best_cost)
        print("global best pos", self.global_best_position)
        t2 = time.time()
        # print("particle generation time: ", round(t2 - t1, 4), "(s)" + "\n")

    def main_loop(self):
        t1 = time.time()

        for it in range(self.max_iter):
            for particle in self.particles:
                p1 = self.w * np.array(particle.velocity)
                r1 = [random.uniform(0, 1) for _ in range(self.var_size)]
                r2 = [random.uniform(0, 1) for _ in range(self.var_size)]
                p2 = self.c1 * np.array(r1) * (np.array(particle.best_position) - np.array(particle.position))
                p3 = self.c2 * np.array(r2) * (np.array(self.global_best_position) - np.array(particle.position))

                # update velocity
                particle.velocity = np.array(p1) + np.array(p2) + np.array(p3)

                # apply velocity limit
                particle.velocity = np.array([max(vel, self.vel_min) for vel in particle.velocity])
                particle.velocity = np.array([min(vel, self.vel_max) for vel in particle.velocity])

                # update position
                particle.position = np.array(particle.position) + np.array(particle.velocity)

                # apply position limit
                particle.position = np.array([max(particle.position[i], self.var_min[i]) for i in range(len(particle.position))])
                particle.position = np.array([min(particle.position[i], self.var_max[i]) for i in range(len(particle.position))])

                # Evaluation
                particle.cost = self.func(particle.position, self.func_data)

                # update personal best
                if particle.cost < particle.best_cost:
                    particle.best_position = particle.position
                    particle.best_cost = particle.cost

                    # update global best
                    if particle.best_cost < self.global_best_cost:
                        self.global_best_cost = particle.best_cost
                        self.global_best_position = particle.best_position
                        print("global_best_cost: ", self.global_best_cost)
                        print("global_best_position: ", self.global_best_position)

            self.best_costs.append(self.global_best_cost)
            self.best_pos.append(self.global_best_position)

            print("iteration", it, ": best cost =", self.global_best_cost)
            print("iteration", it, ": best position =", self.global_best_position)

            self.w *= self.w_damp

            if self.best_costs[it] == 0:
                break

        # --------------- results --------------- #

        t2 = time.time()
        print("Total time of algorithm calculation is:", round(t2 - t1, 4), "(s)")
        # plt.plot(self.best_costs)
        # plt.xlabel('Iteration')
        # plt.ylabel('Best Cost')
        # plt.show()

    def run(self, constriction_coefficient=False):
        self.initialization()
        if constriction_coefficient:
            self.constriction_coefficient()
        self.main_loop()


class Particle:

    def __init__(self):
        self.position = []
        self.cost = 0
        self.velocity = []
        self.best_position = 0
        self.best_cost = 0

    def __str__(self):
        return f"position: {self.position} \n" \
               f"cost: {self.cost} \n" \
               f"velocity: {self.velocity} \n" \
               f"best_position: {self.best_position} \n" \
               f"best_cost: {self.best_cost}"


if __name__ == "__main__":
    height, slope, water_height_left, water_height_right = 12, 1/2.6, 10, 4
    static_data = (height, slope, water_height_left, water_height_right)
    cost = ''
    pso = Pso(0.9, 0.9, 1.4, 0.99, cost, static_data, 40, 100, 4, 4, [7, 10, 20, -10], [12, 15, 30, 10])
    pso.run(constriction_coefficient=True)
    x, y, r, theta = pso.best_pos[-1]
    print("*" * 150)
    print('∑𝑄𝑖 + ∑𝑀𝑖: ', pso.best_costs[-1])
    print("x center circle: ", x)
    print("y center circle: ", y)
    print("radius: ", r)
    Plot.plot(x, y, r)
