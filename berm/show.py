import matplotlib.pyplot as plt
from shapes import Circle


class Trapezoid:
    def __init__(self, height, slope, berms):
        self.height = height
        self.slope = slope
        self.berms = berms
        self.small_base = 0.2 * self.height + 3
        self.big_base = self.small_base + ((2 * self.height) / self.slope)
        self.x0 = 0
        self.x1 = 0

    def main_trapezoid(self):
        self.x0 = self.height / self.slope
        self.x1 = self.x0 + self.small_base
        x = 0, self.x0, self.x1, self.x1 + self.x0
        y = 0, self.height, self.height, 0
        return x, y

    def plot(self):
        x1, y1 = self.main_trapezoid()
        for berm in self.berms:
            h = berm['height']
            a = berm['a']
            s = berm['slope']
            ss = berm['small_side']
            xs = (h * s) + 2 * a
            x = self.x0 - xs, self.x0 - 2 * a, self.x1 + 2 * a, self.x1 + xs
            y = self.height - h, self.height, self.height, self.height - h

            self.x0 -= xs
            self.x1 = self.x1 + xs
            self.height = self.height - h
            plt.plot(x, y)

        plt.plot(x1, y1)
        plt.grid()
        plt.show()


def p_plot(x, y, r, h, s, berms):
    cir = Circle(x, y, r)
    x1, c1 = cir.create()
    plt.plot(x1, c1, 'r', linewidth=0.4)
    tra = Trapezoid(h, s, berms)
    tra.plot()
    plt.show()


if __name__ == '__main__':
    berms_ = [
        {'height': 4, 'a': 0, 'slope': 2, 'small_side': 5.4},
        {'height': 5, 'a': 0.4, 'slope': 2.2, 'small_side': 40},
        {'height': 3, 'a': 0.6, 'slope': 1.6, 'small_side': 40},
    ]
    trap = Trapezoid(12, 1/2.6, berms_)
    # trap.plot()
    p_plot(9, 13, 23, 12, 1/2.6, berms_)
