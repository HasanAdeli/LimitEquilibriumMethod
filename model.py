import random
from utils import *


class CoastFunction:
    def __init__(self):
        self.q_total = 50000
        self.qb_total = 50000

    def cost(self, x, y, r, theta, f):
        # Enter property values
        pm = PropertiesMaterials(20, 2.8, 50, 8, 25)

        # create new circle
        icc = ImportantCoordinatesCircle(x, y, r)
        if not icc.is_valid_circle():
            return self.q_total, self.qb_total

        # Width Slices
        ws = WidthSlices(16, 22, 1, icc)

        # Pore Water Pressure
        pwp = PoreWaterPressure(10, 4, 0.2)

        # End Coordinates Of Slices
        ecs = EndCoordinatesOfSlices(icc, ws, pwp)

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


def cost(data):
    x, y, r, theta, fs = data
    c = CoastFunction()
    q, qb = c.cost(x, y, r, theta, fs)
    return abs(q) + abs(qb) + fs * 100


if __name__ == "__main__":
    pass
