from math import cos, sin
from utility import gravitational_constant, pi, degrees, radians, range_setter, accuracy, time_interval

from functools import lru_cache


# Todo Write my own sin and cos functions
# Todo JSON Initializer
# Todo time interval selector (seconds, minutes, hours, days)
# Todo add a function that gives coords at time = t, add calculate orbit function
# Todo bug fix time = t to complete full orbit (Semi-done)
# Todo add position of focus as argument to angle_to_x, angle_to_y

class Focus:
    """Object around which satellite will  orbit"""
    name = ""
    mass = 0.0
    radius = 0.0
    satellite_list = list()

    def __init__(self, name: str, mass: float, radius: float = 0.0):
        """Initializer for Focus
        :param name: String
        :param mass: Float
        :param radius: Float
        """
        try:
            self.name = str(name)
            self.mass = float(mass)
            self.radius = float(radius)
        except ValueError as e:
            print("An unaccepted variable type was entered, Focus requires Str, Float, Float\n", e)

    def add_to_satellites(self, satellite: object):
        self.satellite_list.append(satellite)


class Satellite:
    """Satellite that will orbit"""

    # # Variables independent from Focus
    # name: str = ""
    # mass: float = 0.0
    #
    # # Variables dependent on Focus
    # focus = None
    # radius: float = 0.0
    # # Calculated variables
    # velocity: float = 0.0
    # period: float = 0.0
    # angular_velocity: float = 0.0

    def __init__(self, name: str, mass: float, focus: Focus = None, radius: float = None, velocity: float = None,
                 period: float = None, angular_velocity: float = None):
        """
        Initializer for Satellite
        :param name: Str
        :param mass: Float
        """
        try:
            # Independent of focus
            self.name = name
            self.mass = mass
            # Dependent of focus
            self.focus = focus
            if focus:
                focus.add_to_satellites(self)
            self.radius = radius
            #     Calculated from focus
            self.velocity = velocity
            self.period = period
            #     Calculated from velocity and radius
            self.angular_velocity = angular_velocity

        except TypeError as e:
            print("An unaccepted variable type was entered, Satellite requires Str, Float\n", e)

    def set_focus(self, focus: Focus, radius: float):
        """
        Sets focus and radius
        :rtype: None
        :param focus: Focus
        :param radius: float
        """
        self.focus = focus
        focus.add_to_satellites(self)
        self.radius = radius

    def calculate_velocity(self) -> float:
        """
        Calculates velocity of a satellite in orbit
        v = sqrt((G * M) / r)
        :return: Velocity
        :rtype: float
        """

        try:
            self.velocity = ((gravitational_constant * self.focus.mass) / self.radius) ** (1 / 2)
        except TypeError as e:
            print(e)
        return self.velocity

    def calculate_period(self) -> float:
        """
        Calculates the period of the satellite (in seconds)
        T = (2 * pi * r) / v
        :return: Period in seconds
        :rtype: Float
        """
        try:
            self.period = (2 * pi * self.radius) / self.velocity
        except Exception as e:
            print("Exception!", e)

        return self.period

    def calculate_angular_velocity(self) -> float:
        """
        Calculates the angular velocity of the satellite rad/ T^-1
        w = v / r
        :rtype: float
        :return: Angular velocity
        """
        try:
            self.angular_velocity = self.velocity / self.radius
        except Exception as e:
            print(e)

        return self.angular_velocity

    @lru_cache(maxsize=None)
    def angle_to_x(self, angle: float) -> float:
        """
        Calculates x coordinate using the following formula:
        X = cos(O(t)) * r
        :rtype: float
        :param angle: float radians
        :return: x-coordinate
        """
        # print(angle)
        return cos(angle) * self.radius

    @lru_cache(maxsize=None)
    def angle_to_y(self, angle: float) -> float:
        """
        Calculates y coordinate using the following formula:
        :rtype: float
        :param angle: float radians
        :return: y-coordinate
        """
        # print(angle)
        return sin(angle) * self.radius

    def angle_to_coordinates(self, period=None) -> tuple:
        """Translates angular position to coordinates (Will be rewritten in next version)
        :rtype: tuple
        :return: y and x coordinates
        """
        # Todo This is truly an abysmal function. Rewrite.
        if not period:
            period = self.period
        # lambda: O(t) = w * t
        angular_positions = map(
            lambda t: round(range_setter(self.angular_velocity * t * time_interval, 0, radians(360)), accuracy),
            range(int(period / time_interval)))
        x_coords, y_coords = list(), list()
        for a_pos in angular_positions:
            # X = cos(O(t)) * r
            x_coords.append(self.angle_to_x(a_pos))
            # Y = sin(O(t)) * r
            y_coords.append(self.angle_to_y(a_pos))
        return y_coords, x_coords

    def __str__(self) -> str:
        return "Name: {}, Mass: {}, Radius: {}, Period: {} Focus: {}, Velocity: {}, Angular Velocity: {}".format(
            self.name,
            self.mass,
            self.radius,
            self.period,
            self.focus,
            self.velocity,
            self.angular_velocity)
