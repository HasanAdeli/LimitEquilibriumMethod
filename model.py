import random
from utils import *
from shapes import Plot


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
            x, y, r = [random.uniform(0, 30) for _ in range(3)]
            if x > r or (y > r or y < 10.8):
                continue
            icc = ImportantCoordinatesCircle(x, y, r)
            if not icc.is_valid_circle():
                continue
            theta = random.uniform(-3, 3)
            # theta = 1
            fs = random.uniform(1.01, 1.8)
            valid_circles.append((x, y, r, theta, fs))
            if len(valid_circles) == length:
                break
        return valid_circles

    @staticmethod
    def get_valid_circles1(length):
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
            theta = random.uniform(-3, 3)
            fs = random.uniform(1.51, 1.58)
            valid_circles.append((x, y, r, theta, fs))
            if len(valid_circles) == length:
                break
        return valid_circles


def cost(data):
    x, y, r, theta, fs = data
    c = CoastFunction()
    q, qb = c.cost(x, y, r, theta, fs)
    return abs(q) + abs(qb) + fs * 10


if __name__ == "__main__":
    pass
    cc = CoastFunction()
    qq, qi = cc.cost(9, 12, 24, 0.3346, 1.521)
    # qq, qi = cost([1.41505193, 1.10827253])
    print(abs(qq) + abs(qi))
