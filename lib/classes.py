from math import cos, sin
from lib.utility import gravitational_constant, pi, radians, range_setter
import json
from functools import lru_cache


# Todo decide on whether or not to save orbits
# Todo bug fix time = t to complete full orbit (Semi-done) Fixed itself?
# Todo add position of focus as argument to angle_to_x, angle_to_y
# TODO add docstring to Focus

class Focus:
    """Object around which satellite will  orbit"""
    name = ""
    mass = 0.0
    radius = 0.0

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
            self.satellite_list = list()
        except ValueError as e:
            print("An unaccepted variable type was entered, Focus requires Str, Float, Float\n", e)

    def add_to_satellites(self, satellite: object):
        if type(satellite) != Satellite:
            raise TypeError

        self.satellite_list.append(satellite)

    def largest_radius(self):
        radii = [x.radius for x in self.satellite_list]
        return max(radii)


class Satellite:
    """Satellite that will orbit"""

    # Todo uncomment, variable expectation annotation?
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

    accuracy: int = 2
    time_interval: int = 1 * 60 * 60  # step size for t in seconds. Base position is 3600 (1 hour)

    def __init__(self, name: str, mass: float, focus: Focus = None, radius: float = None, velocity: float = None,
                 period: float = None, angular_velocity: float = None, orbit: tuple = None):
        """
        Initializer for Satellite
        :param focus: Focus
        :param radius: float
        :param velocity: float
        :param period: float
        :param angular_velocity: float
        :param orbit: list
        :param name: str
        :param mass: float
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
            #     Calculated from angular velocity and radius
            self.orbit = orbit

        except TypeError as e:
            print("An unaccepted variable type was entered, Satellite requires Str, Float\n", e)

    def to_json(self, filename: str = None, save_orbit: bool = False):
        """
        Dumps satellite and focus data to JSON
        :param save_orbit: bool
        :param filename: str
        """

        # If no filename is given, use satellite name as name
        if not filename:
            filename = self.name

        data = dict()
        data['name'] = self.name
        data['mass'] = self.mass
        data['focus'] = dict()
        data['focus']['name'] = self.focus.name
        data['focus']['mass'] = self.focus.mass
        data['radius'] = self.radius
        data['velocity'] = self.velocity
        data['period'] = self.period
        data['angular_velocity'] = self.angular_velocity
        data['orbit'] = dict()
        data['orbit']['time_interval'] = self.time_interval
        data['orbit']['accuracy'] = self.accuracy
        data['orbit']['coordinates'] = dict()
        # If an orbit has been calculated and the user wants to save orbit, save orbit to JSON
        if self.orbit and save_orbit:
            print("Warning, it is not recommended to save orbit to JSON. Loading in the orbits from JSON causes errors "
                  "due to size")
            data['orbit']['coordinates']['x'] = self.orbit[0]
            data['orbit']['coordinates']['y'] = self.orbit[1]
        else:
            data['orbit']['coordinates']['x'] = []
            data['orbit']['coordinates']['y'] = []

        with open(filename + '.json', 'w') as outfile:
            json.dump(data, outfile, indent=4)

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

    def angle_to_x(self, angle: float) -> float:
        """
        Calculates x coordinate using the following formula:
        X = cos(O(t)) * r
        :rtype: float
        :param angle: float radians
        :return: x-coordinate
        """
        return cos(angle) * self.radius

    def angle_to_y(self, angle: float) -> float:
        """
        Calculates y coordinate using the following formula:
        :rtype: float
        :param angle: float radians
        :return: y-coordinate
        """
        return sin(angle) * self.radius

    def angular_position_at_t(self):
        """
        Returns lambda that calculates angular position at time index t.
        O(t) = wt
        """
        # Todo explain time interval
        return lambda t: round(range_setter(self.angular_velocity * t * self.time_interval, radians(360)),
                               self.accuracy)

    @lru_cache(maxsize=None)
    def angular_position_to_coordinates(self, angular_position: float) -> tuple:
        """
        Calculates X,Y coordinates with angular position. Calls angle_to_y and angle_to_x
        :return: x,y
        :param angular_position:
        :rtype: tuple
        """
        x = self.angle_to_x(angular_position)
        y = self.angle_to_y(angular_position)
        return x, y

    def calculate_orbit(self, period: float = None) -> list:
        """
        Calculates all orbital coordinates
        :param period: float
        :return: orbit
        """
        # If no period is given, set period to self.period
        if not period:
            period = self.period

        # Initialize two-dimensional list for orbit
        orbit = [[], []]

        # Generate a map of angular_positions for given period
        # Todo explain time interval

        angular_pos = map(self.angular_position_at_t(), range(int(period / self.time_interval) + 1))
        # For each angular position, generate x,y coordinates, append coordinates to orbit
        for angle in angular_pos:
            x, y = self.angular_position_to_coordinates(angle)
            orbit[0].append(x)
            orbit[1].append(y)
        self.orbit = orbit
        return orbit

    def __str__(self) -> str:
        return "Name: {}, Mass: {}, Radius: {}, Period: {} Focus: {}, Velocity: {}, Angular Velocity: {}".format(
            self.name,
            self.mass,
            self.radius,
            self.period,
            self.focus,
            self.velocity,
            self.angular_velocity)


def json_satellite_construct(file_string: str) -> tuple:
    """
    :rtype: tuple
    :param file_string: str
    :return: a tuple containing a satellite and a focus
    """
    with open(file_string + '.json') as satellite_json:
        data = json.load(satellite_json)

    # Get satellite data
    sat_name = data['name']
    sat_mass = data['mass']
    sat_radius = data['radius']
    sat_velocity = data['velocity']
    sat_period = data['period']
    sat_angular_velocity = data['angular_velocity']
    sat_orbit = data['orbit']['coordinates']['x'], data['orbit']['coordinates']['y']

    # Get focus data
    focus_name = data['focus']['name']
    focus_mass = data['focus']['mass']
    #  Construct focus and satellite
    focus = Focus(focus_name, focus_mass)
    sat = Satellite(sat_name, sat_mass, focus, sat_radius, sat_velocity, sat_period, sat_angular_velocity, sat_orbit)

    # Get independent variables
    sat_time_interval = data['orbit']['time_interval']
    sat_accuracy = data['orbit']['accuracy']

    # Set independent variables
    sat.time_interval = sat_time_interval
    sat.accuracy = sat_accuracy

    return sat, focus
