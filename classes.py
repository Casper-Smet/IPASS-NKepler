from matplotlib import pyplot as plt
from math import cos, sin
from utility import gravitational_constant, pi, degrees, radians, range_setter, accuracy

from functools import lru_cache


# Todo Remove real_distance, initialize with radius

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


class Satellite:
    """Satellite that will orbit"""
    # Variables independent from Focus
    name: str = ""
    mass: float = 0.0
    radius: float
    # Variables dependent on Focus
    focus = None
    distance_to_focus: float = 0.0
    real_distance: float = 0.0
    # Calculated variables
    velocity: float = 0.0
    period: float = 0.0
    angular_velocity: float = 0.0

    def __init__(self, name: str, mass: float, radius: float = 0.0):
        """
        Initializer for Satellite
        :param name: Str
        :param mass: Float
        :param radius: Float
        """
        try:
            self.name = name
            self.mass = mass
            self.radius = radius
        except TypeError as e:
            print("An unaccepted variable type was entered, Satellite requires Str, Float, Float\n", e)

    def set_focus(self, focus: Focus, distance_to_focus: float):
        """
        Sets focus and distance to focus, calculates 'real_distance'
        :rtype: None
        :param focus: Focus
        :param distance_to_focus: float
        """
        self.focus = focus
        self.distance_to_focus = distance_to_focus

        self.real_distance = self.focus.radius + self.radius + self.distance_to_focus

    def calculate_velocity(self) -> float:
        """
        Calculates velocity of a satellite in orbit
        v = sqrt((G * M) / r)
        :return: Velocity
        :rtype: float
        """

        try:
            self.velocity = ((gravitational_constant * self.focus.mass) / self.real_distance) ** (1 / 2)
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
            self.period = (2 * pi * self.real_distance) / self.velocity
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
            self.angular_velocity = self.velocity / self.real_distance
        except Exception as e:
            print(e)

        return self.angular_velocity

    @lru_cache(maxsize=int(period) + 1)
    def angle_to_x(self, angle: float) -> float:
        """
        Calculates x coordinate using the following formula:
        X = cos(O(t)) * r
        :rtype: float
        :param angle: float radians
        :return: x-coordinate
        """
        return cos(angle) * self.real_distance

    @lru_cache(maxsize=int(period) + 1)
    def angle_to_y(self, angle: float) -> float:
        """
        Calculates y coordinate using the following formula:
        :rtype: float
        :param angle: float radians
        :return: y-coordinate
        """
        return sin(angle) * self.real_distance

    def angle_to_coordinates(self, period=None) -> tuple:
        """Translates angular position to coordinates
        :rtype: tuple
        :return: y and x coordinates
        """
        if not period:
            period = self.period
        # lambda: O(t) = w * t
        angular_positions = map(lambda t: round(range_setter(self.angular_velocity * t, 0, radians(360)), accuracy),
                                range(int(period)))
        x_coords, y_coords = list(), list()
        for a_pos in angular_positions:
            # X = cos(O(t)) * r
            x_coords.append(self.angle_to_x(a_pos))
            # Y = sin(O(t)) * r
            y_coords.append(self.angle_to_y(a_pos))
        return y_coords, x_coords

    def __str__(self) -> str:
        return "Name: {}, Mass: {}, Radius: {}, Focus: {}, Distance to Focus: {}, Velocity: {}".format(self.name,
                                                                                                       self.mass,
                                                                                                       self.radius,
                                                                                                       self.focus,
                                                                                                       self.distance_to_focus,
                                                                                                       self.velocity)
