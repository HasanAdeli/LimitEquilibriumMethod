import math
import matplotlib.pyplot as plt


class Circle:
    def __init__(self, x_center_circle, y_center_circle, radius):
        self.x_center_circle = x_center_circle
        self.y_center_circle = y_center_circle
        self.radius = radius

    def calculate(self, x):
        try:
            y1 = math.sqrt(self.radius ** 2 - (x - self.x_center_circle) ** 2) + self.y_center_circle
            y2 = -math.sqrt(self.radius ** 2 - (x - self.x_center_circle) ** 2) + self.y_center_circle
        except:
            print(2)

        return y1, y2

    def create(self):
        circle1 = []
        xs = []
        self.x_center_circle = round(self.x_center_circle, 4)
        self.radius = round(self.radius, 4)
        x = round(self.x_center_circle - self.radius, 4)
        while x < self.x_center_circle + self.radius:
            circle1.append(self.calculate(x)[0])
            xs.append(x)
            x += 0.001
            x = round(x, 4)
        x = round(self.x_center_circle + self.radius, 4)
        while x > self.x_center_circle - self.radius:
            circle1.append(self.calculate(x)[1])
            xs.append(x)
            x -= 0.001
            x = round(x, 4)
        return xs, circle1

    def cut(self):
        x1, y1 = self.create()
        semicircular_x = []
        semicircular_y = []
        for x, y in zip(x1, y1):
            if 0 < x < 40 and 0 < y < 12:
                semicircular_x.append(x)
                semicircular_y.append(y)
            if 40 > x > 0 > y:
                semicircular_x.append(x)
                semicircular_y.append(y)
            elif x < 0 and y < 0:
                semicircular_x.append(x)
                semicircular_y.append(y)
        return semicircular_x, semicircular_y

    @staticmethod
    def slicing(x, y):
        plt.plot(x, y, 'r')
        plt.grid()
        plt.show()

    def plot(self):
        y1, x1 = self.create()
        plt.plot(x1, y1, 'r')
        plt.grid()
        plt.show()


class Trapezoid:
    def __init__(self, height, slope):
        self.height = height
        self.slope = slope
        self.small_base = 0.2 * self.height + 3
        self.big_base = self.small_base + ((2 * self.height) / self.slope)

    def create(self):
        xs = self.height / self.slope
        xe = xs + self.small_base
        x = 0, xs, xe, xe + xs
        y = 0, self.height, self.height, 0
        return x, y

    def plot(self):
        x, y = self.create()
        plt.plot(x, y)
        plt.grid()
        plt.show()


class Plot:
    @staticmethod
    def plot(x, y, r, height, slope):
        cir = Circle(x, y, r)
        x1, c1 = cir.create()
        x11, c11 = cir.cut()
        tra = Trapezoid(height, slope)
        x2, y2 = tra.create()
        plt.fill_between(x2, y2)
        plt.plot(x1, c1, 'r', linewidth=0.4)
        plt.plot(x11, c11, 'r', linewidth=1.5)
        plt.plot([0, 0], [min(c1) - 10, max(c1) + 10], 'k', linewidth=0.8)
        plt.plot([min(x1) - 10, max(x2) + 10], [0, 0], 'k', linewidth=0.8)
        plt.xlim(min(x1) - 10, max(x2) + 10)
        plt.ylim(min(c1) - 10, max(c1) + 10)
        plt.show()


if __name__ == "__main__":
    Plot.plot(9.56948994, 13.82831293, 23.81828731)
#     cir = Circle(4.4066, 6.9814, 27.028)
#     x1, c1 = cir.create()
#     x11, c11 = cir.cut()
#     tra = Trapezoid(12, 1/2.6)
#     x, y = tra.create()
#     plt.fill_between(x, y)
#     plt.plot(x1, c1, 'r', linewidth=0.4)
#     plt.plot(x11, c11, 'r', linewidth=1.5)
#     # plt.plot(x, y, 'b')
#
#     plt.plot([0, 0], [min(c1)-10, max(c1)+10], 'k', linewidth=0.8)
#     plt.plot([min(x1)-10, max(x)+10], [0, 0], 'k', linewidth=0.8)
#     plt.xlim(min(x1)-10, max(x)+10)
#     plt.ylim(min(c1)-10, max(c1)+10)
#     plt.show()

"""
[ 9.84119803 11.23332412 25.50968209  1.41505193  1.10827253]

valid : 4.4066, 6.9814, 27.028
theta = -2.243635, f = 1.51

11.62208232 13.04056997 27.83296453

7.105947681574937 20.91361540695176 25.06079970909294
x1:  20.91407473303933
x2:  -6.702179369889457
x3:  30.035371256090293
"""