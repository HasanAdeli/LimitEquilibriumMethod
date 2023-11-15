import math


# 1) Characteristics Of SlopeGeometry Attribute
class SlopeGeometryAttribute:
    GAMMA_WET = 18
    GAMMA_WATER = 9.81
    GAMMA_SAT = 20

    def __init__(self, height, slope, water_height_left, water_height_right):
        self.height = height
        self.slope = slope
        self.water_height_left = water_height_left
        self.water_height_right = water_height_right
        self.side_small = 0.2 * height + 3
        self.side_big = self.side_small + ((2 * height) / slope)
        self.beta = math.atan(slope)
        self.max_range = height / math.tan(self.beta)  # start
        self.height_div_slope = height / slope
        self.side_small_sum_height_div_slope = self.side_small + self.height_div_slope  # end


# 2) Properties Materials
class PropertiesMaterials:
    def __init__(self, gamma_sat, gs, drained_cohesion, drained_friction_angle, bedrock_height):
        # a = (20, 2.8, 50, 8, 25)
        self.gamma_watter = 9.81
        self.gamma_sat = gamma_sat
        self.gs = gs
        self.drained_cohesion = drained_cohesion  # c_prime
        self.drained_friction_angle = drained_friction_angle  # phi_prime
        self.bedrock_height = bedrock_height

        self.gamma_sat_div_gamma_watter = self.gamma_sat / self.gamma_watter


class ImportantCoordinatesCircle:
    def __init__(self, x_center_circle, y_center_circle, radius, sga):
        self.x_center_circle = x_center_circle
        self.y_center_circle = y_center_circle
        self.radius = radius
        self.sga = sga
        self.intersection_horizontal_axis_and_slip_surface_left = 0
        self.intersection_horizontal_axis_and_slip_surface_right = 0
        self.intersection_embankment_and_slip_surface = 0
        self.error = False

    def computing(self):
        intersection_horizontal = math.sqrt(self.radius ** 2 - self.y_center_circle ** 2)
        self.intersection_horizontal_axis_and_slip_surface_left = -intersection_horizontal + self.x_center_circle
        self.intersection_horizontal_axis_and_slip_surface_right = intersection_horizontal + self.x_center_circle

        intersection_embankment_and_slip_surface = math.sqrt(self.radius ** 2 - ((0.9 * self.sga.height - self.y_center_circle) ** 2))
        self.intersection_embankment_and_slip_surface = intersection_embankment_and_slip_surface + self.x_center_circle

    def is_valid_circle(self):
        try:
            self.computing()
        except Exception as err:
            self.error = err
            return False
        condition1 = self.intersection_horizontal_axis_and_slip_surface_left < 0
        condition2 = 0 < self.intersection_horizontal_axis_and_slip_surface_right < self.sga.side_big
        condition3 = 0.88 * self.sga.max_range < self.intersection_embankment_and_slip_surface < self.sga.max_range + self.sga.side_small
        if condition1 and condition2 and condition3:
            return True
        return False

    def penalty_amount(self):
        if self.error:
            return 100000, 0
        amount = 1
        penalty = 100
        if self.intersection_horizontal_axis_and_slip_surface_left >= 0:
            amount *= (1 + self.intersection_horizontal_axis_and_slip_surface_left) * penalty
        if self.intersection_horizontal_axis_and_slip_surface_right <= 0:
            amount *= (1 + self.intersection_horizontal_axis_and_slip_surface_right) * penalty
        if self.intersection_horizontal_axis_and_slip_surface_right > self.sga.side_big:
            amount *= (1 + abs(self.intersection_horizontal_axis_and_slip_surface_right / self.sga.side_big)) * penalty
        if self.intersection_embankment_and_slip_surface <= 0.88 * self.sga.max_range:
            amount *= (1 + abs(self.intersection_embankment_and_slip_surface / 0.88 * self.sga.max_range)) * penalty * 100
        if self.intersection_embankment_and_slip_surface >= self.sga.max_range + self.sga.side_small:
            amount *= (1 + abs(self.intersection_embankment_and_slip_surface / self.sga.max_range + self.sga.side_small)) * penalty * 100
        return amount, 0


# 5.1) Width Slices
class WidthSlices:
    def __init__(self, number_slices_first_piece, number_slices_second_piece, number_slices_third_piece, icc, sga):
        self.icc = icc
        self.sga = sga
        self.number_slices_first_piece = number_slices_first_piece
        self.number_slices_second_piece = number_slices_second_piece
        self.number_slices_third_piece = number_slices_third_piece
        self.number_of_slices = number_slices_first_piece + number_slices_second_piece + number_slices_third_piece
        self.__computing()

    def __computing(self):
        numerator_first_piece = 0 - self.icc.intersection_horizontal_axis_and_slip_surface_left
        numerator_second_piece = self.sga.height / math.tan(self.sga.beta) * 0.88
        numerator_third_piece = self.icc.intersection_embankment_and_slip_surface - numerator_second_piece

        self.width_first_piece = numerator_first_piece / self.number_slices_first_piece
        self.width_second_piece = numerator_second_piece / self.number_slices_second_piece
        self.width_third_piece = numerator_third_piece / self.number_slices_third_piece


class PoreWaterPressure:
    def __init__(self, hwl, hwr, hg):
        self.hwl = hwl       # Water Height Left
        self.hwr = hwr       # Water Height Right
        self.hg = hg         # hydraulic Gradient
        self.yw1 = 0
        self.yw2 = 0
        self.yw3 = 0
        self.__computing()

    def __computing(self):
        pass


class EndCoordinatesOfSlices:
    def __init__(self, icc, ws, pwp, sga):
        self.x_indexes = [0]
        self.y_indexes = [0]
        self.y2_indexes = [0]
        self.y3_indexes = [0]
        self.results = []
        self.weight = 0
        self.icc = icc
        self.ws = ws
        self.pwp = pwp
        self.sga = sga
        self.__computing()

    def __computing(self):
        x_index = self.icc.intersection_horizontal_axis_and_slip_surface_left
        y_index, xb_index, yb_index, alpha_index, delta_index, force_vertical, area_index = 0, 0, 0, 0, 0, 0, 0
        for indexSlice in range(self.ws.number_of_slices):
            if x_index < 0:
                x_index = x_index + self.ws.width_first_piece
                xb_index = (self.ws.number_slices_first_piece - 1) * self.ws.width_first_piece + self.ws.width_first_piece / 2

                y_index = self.get_y(x_index)
                yb_index = self.get_y(xb_index)

                area_index = abs((self.y_indexes[-1] + y_index) / 2 * self.ws.width_first_piece)
                alpha_index = math.atan((y_index - self.y_indexes[-1]) / (x_index - self.x_indexes[-1]))

                delta_index = self.ws.width_first_piece / math.cos(alpha_index)
                force_vertical = self.sga.GAMMA_WET * area_index

            elif 0 <= x_index < self.sga.max_range * 0.88:
                x_index = x_index + self.ws.width_second_piece
                xb_index = (self.ws.number_slices_second_piece - 1) * self.ws.width_second_piece + self.ws.width_second_piece / 2

                y12_index = self.sga.slope * x_index
                y_index = self.get_y(x_index)
                yb_index = self.get_y(xb_index)

                area_index = (self.y_indexes[-1] + y_index) / 2 * self.ws.width_second_piece +\
                             (self.y2_indexes[-1] + y12_index) / 2 * self.ws.width_second_piece
                alpha_index = math.atan((y_index - self.y_indexes[-1]) / (x_index - self.x_indexes[-1]))

                delta_index = self.ws.width_first_piece / math.cos(alpha_index)
                force_vertical = self.sga.GAMMA_WET * area_index
                self.y2_indexes.append(y12_index)

            elif x_index >= self.sga.max_range * 0.88:
                x_index = x_index + self.ws.width_third_piece
                xb_index = (self.ws.number_slices_third_piece - 1) * self.ws.width_third_piece + self.ws.width_third_piece / 2

                y12_index = self.sga.slope * x_index
                y_index = self.get_y(x_index)
                yb_index = self.get_y(xb_index)

                area_index = (self.y_indexes[-1] + y_index) / 2 * self.ws.width_third_piece + \
                             (self.y3_indexes[-1] + y12_index) / 2 * self.ws.width_third_piece
                alpha_index = math.atan((y_index - self.y_indexes[-1]) / (x_index - self.x_indexes[-1]))

                delta_index = self.ws.width_first_piece / math.cos(alpha_index)
                force_vertical = self.sga.GAMMA_WET * area_index
                self.y3_indexes.append(y12_index)

            u = self.get_pwp(x_index, y_index)
            self.weight += self.sga.GAMMA_SAT * area_index
            self.x_indexes.append(x_index)
            self.y_indexes.append(y_index)
            self.results.append((alpha_index, delta_index, force_vertical, xb_index, yb_index, u))

    def get_y(self, x_index):
        sqr = self.icc.radius ** 2 - (x_index - self.icc.x_center_circle) ** 2

        try:
            y1_index = math.sqrt(sqr) + self.icc.y_center_circle
            y2_index = -math.sqrt(sqr) + self.icc.y_center_circle
        except:
            y1_index = self.icc.y_center_circle
            y2_index = -self.icc.y_center_circle

        if y1_index < 0 and y2_index < 0:
            return 0
        elif y1_index >= 0 > y2_index:
            return y2_index
        elif y2_index >= 0 > y1_index:
            return y1_index
        elif y1_index >= 0 and y2_index >= 0:
            return min(y1_index, y2_index)

    def get_pwp(self, x_index, y_index):
        h_index = 0
        self.pwp.yw3 = self.pwp.hg * (x_index - self.pwp.hwl / self.sga.slope)
        if x_index <= self.pwp.hwl / self.sga.slope:
            h_index = self.pwp.hwl + (abs(self.y_indexes[-1]) + abs(y_index)) / 2
        elif self.pwp.hwl / self.sga.slope < x_index < self.icc.intersection_horizontal_axis_and_slip_surface_right:
            h_index = self.pwp.yw3 + (abs(self.y_indexes[-1]) + abs(y_index)) / 2
        elif self.icc.intersection_horizontal_axis_and_slip_surface_right < x_index <= self.icc.intersection_embankment_and_slip_surface + 0.001:
            h_index = self.pwp.yw3 - (abs(self.y_indexes[-1]) + abs(y_index)) / 2

        pwp_index = abs(h_index) * self.sga.GAMMA_WATER
        return pwp_index


class HorizontalForce:
    def __init__(self, m, a_max, weight):
        self.m = m
        self.a_max = a_max
        self.weight = weight
        self.measured_intensity = [6.5, 7, 7.5, 8.25]
        self.earthquake_coefficient = [1.5, 1.4, 1.3, 1.2]
        self.__computing()

    def __computing(self):
        earthquake_coefficient = 0
        for mi, ec in zip(self.earthquake_coefficient, self.measured_intensity):
            if mi == self.m:
                earthquake_coefficient = ec

        a_h = earthquake_coefficient * self.a_max
        self.force_horizontal = a_h * self.weight


class Q:
    def __init__(self, ecs, pm, hf):
        self.pm = pm
        self.ecs = ecs
        self.hf = hf

    def get_q(self, alpha, delta, force_vertical, u, theta, fs):
        force_horizontal = self.hf.force_horizontal
        part1 = -force_vertical * math.sin(alpha) - force_horizontal * math.cos(alpha)
        part2 = self.pm.drained_cohesion * delta / fs
        part3 = -force_vertical * math.cos(alpha) - force_horizontal * math.sin(alpha) + delta * u
        part4 = math.tan(self.pm.drained_friction_angle) / fs
        part5 = math.cos(alpha - theta)
        part6 = math.sin(alpha - theta) * math.tan(self.pm.drained_friction_angle) / fs
        q = (part1 - part2 + part3 * part4) / (part5 + part6)
        return q

    @staticmethod
    def get_qb(q, xb, yb, theta):
        return q * (xb * math.sin(theta) - yb * math.cos(theta))

    def total_q(self, theta, f):
        q_total = 0
        qb_total = 0
        for res in self.ecs.results:
            q = self.get_q(res[0], res[1], res[2], res[5], theta, f)
            qb = self.get_qb(q, res[3], res[4], theta)
            q_total += q
            qb_total += qb
        return q_total, qb_total

    def get_fs(self):
        fs = 1.54
        while fs <= 10:
            q_total, qb_total = self.total_q(0, fs)
            # print(q_total + qb_total)
            if -10 < q_total + qb_total < 10:
                return fs
            fs += 0.1
        return fs
