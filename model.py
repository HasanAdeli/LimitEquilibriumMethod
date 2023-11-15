import random
from utils import *
from pso_algorithm import Pso
from shapes import Plot


class CoastFunction:
    def __init__(self):
        self.q_total = 5000
        self.qb_total = 5000

    def cost(self, x, y, r, theta, static_data):

        f, *static_data = static_data

        # Slope Geometry Attribute
        sga = SlopeGeometryAttribute(*static_data)

        # Enter property values
        pm = PropertiesMaterials(20, 2.8, 50, 8, 25)

        # create new circle
        icc = ImportantCoordinatesCircle(x, y, r, sga)
        if not icc.is_valid_circle():
            self.q_total, self.qb_total = icc.penalty_amount()
            return self.q_total, self.qb_total

        # Width Slices
        ws = WidthSlices(16, 22, 1, icc, sga)

        # Pore Water Pressure
        pwp = PoreWaterPressure(10, 4, 0.2)

        # End Coordinates Of Slices
        ecs = EndCoordinatesOfSlices(icc, ws, pwp, sga)

        # HorizontalForce
        hf = HorizontalForce(6.5, 1, ecs.weight)

        # Q equation
        q = Q(ecs, pm, hf)
        self.q_total, self.qb_total = q.total_q(theta, f)
        return self.q_total, self.qb_total

    @staticmethod
    def get_valid_circles(length):
        valid_circles = []
        while True:
            x = random.uniform(6, 12)
            y = random.uniform(10, 15)
            r = random.uniform(20, 30)
            if x > r or (y > r or y < 10.8):
                continue
            icc = ImportantCoordinatesCircle(x, y, r)
            if not icc.is_valid_circle():
                continue
            theta = random.uniform(-10, 10)
            fs = random.uniform(1, 10)
            valid_circles.append((x, y, r, theta, fs))
            if len(valid_circles) == length:
                break
        return valid_circles


def cost(data, static_data):
    x, y, r, theta = data
    c = CoastFunction()
    q, qb = c.cost(x, y, r, theta, static_data)
    return abs(q + qb)


def get_cost(fs, height, slope, water_height_left, water_height_right):
    static_data = (fs, height, slope, water_height_left, water_height_right)

    pso = Pso(0.9, 0.9, 1.4, 0.99, cost, static_data, 100, 350, 4, 4, [0, 0, 1, -10], [20, 25, 45, 10])
    pso.run(constriction_coefficient=True)
    print('∑𝑄𝑖 + ∑𝑀𝑖: ', pso.best_costs[-1])
    # x, y, r, theta = pso.best_pos[-1]
    # print("x center circle: ", x)
    # print("y center circle: ", y)
    # print("radius: ", r)
    # Plot.plot(x, y, r, height, slope)
    return pso.best_costs[-1]


if __name__ == '__main__':
    # result = get_cost(1.3, 12, 1/2.6, 10, 4)
    result = get_cost(1.3, 3, 1.68, 10, 4)
    # static_data = (1.3, 3, 1/2.6, 10, 4)
    # cost((4.484826560531445, 1.7284193840573927, 5.013628514001555, 2.8891), static_data)
    '''
    x center circle:  4.484826560531445
y center circle:  1.7284193840573927
radius:  5.013628514001555
theta: 2.8891
    '''
