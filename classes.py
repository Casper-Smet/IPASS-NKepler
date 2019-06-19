from matplotlib import pyplot as plt
from math import cos, sin
from kepler import range_setter
from utility import gravitational_constant, pi, degrees, radians


# Todo position at T = 0
# Todo angular velocity w=(v/r), O(t) = O + wt,
# The vector for a position at time T is (cos(O(T)) * r, sin(O(T)) * r) if you want T=0 to be (r, 0)
class Focus:
    """Object around which satellite will  orbit"""
    name = ""
    mass = 0.0
    radius = 0.0
    satellite_list = list()

    def __init__(self, name, mass, radius=0.0):
        """Initializer for Focus"""
        try:
            self.name = str(name)
            self.mass = float(mass)
            self.radius = float(radius)
        except ValueError as e:
            print("An unaccepted variable type was entered, Focus requires Str, Float, Float\n", e)


class Satellite:
    """Satellite that will orbit"""
    # Variables independent from Focus
    name = ""
    mass = 0.0
    radius = 0.0

    focus = None
    distance_to_focus = 0.0
    real_distance = 0.0

    velocity = 0.0
    period = 0.0
    angular_velocity = 0.0

    def __init__(self, name, mass, radius=0.0):
        """Initializer for Satellite"""
        try:
            self.name = name
            self.mass = mass
            self.radius = radius
        except TypeError as e:
            print("An unaccepted variable type was entered, Satellite requires Str, Float, Float\n", e)

    def set_focus(self, focus, distance_to_focus):
        self.focus = focus
        self.distance_to_focus = distance_to_focus

        self.real_distance = self.focus.radius + self.radius + self.distance_to_focus

    def calculate_velocity(self):
        """Calculates velocity of a satellite in orbit"""
        real_distance = self.focus.radius + self.radius + self.distance_to_focus

        try:
            self.velocity = ((gravitational_constant * self.focus.mass) / real_distance) ** (1 / 2)
        except TypeError as e:
            print(e)
        return self.velocity

    def calculate_period(self):
        """Calculates the period of the satellite (in seconds)
        :rtype: Float
        """
        real_distance = self.focus.radius + self.radius + self.distance_to_focus
        try:
            self.period = (2 * pi * real_distance) / self.velocity
        except Exception as e:
            print("Exception!", e)

        return self.period

    def map_positions(self):
        time_list = range(int(self.period) * 2)
        orbit_list = list()
        # orbit_list = map(lambda t: (t * self.angular_velocity), time_list)
        for i in time_list:
            angl = degrees(i * self.angular_velocity)
            # if angl > 360:
            #     print(angl)
            orbit_list.append(range_setter(angl, 0, 360))

        plt.plot(list(orbit_list))
        plt.show()

    def calculate_angular_velocity(self):
        """Calculates the angular velocity of the satellite rad T^-1"""
        try:
            self.angular_velocity = self.velocity / self.real_distance
        except Exception as e:
            print(e)

        return self.angular_velocity

    def calculate_angular_position(self):
        """Calculates angular position using angular velocity:
        O(t) = O + w * t"""
        try:
            return lambda t: self.angular_velocity * t
        except Exception as e:
            print(e)

    def angle_to_coordinates(self):
        """Translates angular position to coordinates"""
        angular_positions = map(lambda t: self.angular_velocity * t, range(int(self.period)))
        x_coords, y_coords = list(), list()
        for a_pos in angular_positions:
            x_coords.append(cos(a_pos) * self.real_distance)
            y_coords.append(sin(a_pos) * self.real_distance)
        return y_coords, x_coords

    def __str__(self) -> str:
        return "Name: {}, Mass: {}, Radius: {}, Focus: {}, Distance to Focus: {}, Velocity: {}".format(self.name,
                                                                                                       self.mass,
                                                                                                       self.radius,
                                                                                                       self.focus,
                                                                                                       self.distance_to_focus,
                                                                                                       self.velocity)


if __name__ == '__main__':
    sat1 = Satellite("Sat1", 0.0)
    plt1 = Focus("Earth", 5.97 * 10 ** 24, 6.38 * 10 ** 6)

    sat1.set_focus(plt1, 3800 * 10 ** 3)

    plt2 = Focus("Earth2", 5.972 * 10 ** 24)
    sat2 = Satellite("Moon", 0, 0)

    sat2.set_focus(plt2, 384.4 * 10 ** 6)

    print("Velocity in m s^-1:", sat2.calculate_velocity())
    print("Period in s:", sat2.calculate_period())
    print("Angular velocity in radians s^-1:", sat2.calculate_angular_velocity())

    print(sat2.angle_to_coordinates())
