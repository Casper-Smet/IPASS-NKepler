from math import cos, sin, atan2
from lib.utility import gravitational_constant, pi, range_setter, time_difference
from datetime import datetime as dt
import json
from functools import lru_cache

# TODO Add location at date; see plan below:
"""Plan: 
    1. Add date and possibly known position to initializer, make a separate setter for date + location (angular or 
    euclidean coordinates?). 
    2. Adding delta t to angular_position_at_t might be enough?
Extra's:
    1e. Add delta date calculator.

Things to figure out:
    1f. Data for planetary positions (T-SSAT?)
    2f. Static standard date, or different date for each different satellite. Non-static is most likely candidate, but
    will be significantly harder to program. 
"""
# Todo add position of focus as argument to angle_to_x, angle_to_y; see plan below
"""Plan:
    1. Rewrite Satellite to accept Satellite as a focus.
        a. OPTIONAL; delete Focus in its entirety 
    2. Add satellite_list to Satellite
    2. Add optional 'current_focus_coordinates variable'.
        a. Either angle_to_x, angle_to_y
        b. Angular_position_to_coordinates
        c. Conglomerate orbit function
Extra's:
    1e. Add satellite of satellite to simulations
        a. Add moon to sim_solar_system     
        b. Make separate model of moon around earth around sun
        c. Add Jupiter's moons to sim_solar_system 
"""


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
        """
        Adds satellite to satellite_list
        :param satellite:
        """
        if type(satellite) != Satellite:
            raise TypeError

        self.satellite_list.append(satellite)

    def largest_radius(self) -> float:
        """
        Returns the value of the biggest radius in satellite_list
        :rtype: float
        :return biggest radius:
        """
        if self.satellite_list:
            radii = [x.radius for x in self.satellite_list]
            return max(radii)
        else:
            print("Satellite_list is empty")
            return 0.0


class Satellite:
    """Satellite that will orbit"""

    # Variables independent from Focus
    name: str
    mass: float

    # Variables dependent on Focus
    focus: Focus
    radius: float
    # Calculated variables
    velocity: float
    period: float
    angular_velocity: float

    # Date related variables
    known_date_s: float
    known_date_dt: dt
    # known_coordinates: list
    # known_angular_position: float

    accuracy: int = 2
    time_interval: int = 1 * 60 * 60  # step size for t in seconds. Base position is 3600 (1 hour)

    def __init__(self, name: str, mass: float, focus: Focus = None, radius: float = None, velocity: float = None,
                 period: float = None, angular_velocity: float = None, known_date_s: float = None,
                 known_date_dt: dt = None, orbit: tuple = None):
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
            # Date related variables
            self.known_date_s = known_date_s
            self.known_date_dt = known_date_dt

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

    def set_origin(self, known_date_dt: dt, coordinates: list):
        # TODO docstrings
        # TODO exceptions
        self.known_date_dt = known_date_dt
        self.calculate_t_for_position(coordinates, True)
        print(f"{self.known_date_dt} equals {self.known_date_s}")

    def update_origin(self, updated_date: dt):
        # Earliest possible t where the satellite is in the same relative position
        # TODO docstrings
        # TODO exceptions
        large_time = self.known_date_s + time_difference(self.known_date_dt, updated_date)
        angular_position = self.angular_position_at_t()(large_time)
        accurate_time = self.t_from_angular_position(angular_position)
        self.known_date_s = accurate_time
        self.known_date_dt = updated_date
        print(f"{self.known_date_dt} equals {self.known_date_s}")
        return self.known_date_s

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
        if type(angle) not in [int, float]:
            raise TypeError

        return cos(angle) * self.radius

    def angle_to_y(self, angle: float) -> float:
        """
        Calculates y coordinate using the following formula:
        y = sin(O(t)) * r
        :rtype: float
        :param angle: float radians
        :return: y-coordinate
        """
        if type(angle) not in [int, float]:
            raise TypeError
        return sin(angle) * self.radius

    def coordinates_to_angle(self, coordinates: list):
        # TODO docstrings
        # TODO exceptions
        # TODO non-static middle_point
        if type(coordinates) not in [list, tuple]:
            raise TypeError

        middle_point = [0, 0]
        return range_setter(atan2(coordinates[1] - middle_point[1], coordinates[0] - middle_point[0]),
                            6.283185307180001)

    def angular_position_at_t(self, from_known: bool = False):
        """
        Returns lambda that calculates angular position at time index t.
        O(t) = wt
        """

        # Time interval is the amount of time that passes per t in seconds
        if from_known:
            return lambda t: round(
                range_setter(self.angular_velocity * (t * self.time_interval + self.known_date_s), 6.283185307180001),
                self.accuracy)
        else:
            return lambda t: round(
                range_setter(self.angular_velocity * t * self.time_interval, 6.283185307180001), self.accuracy)

    def t_from_angular_position(self, angular_position: float) -> float:
        # TODO docstrings
        if type(angular_position) not in [float, int]:
            raise TypeError
        return angular_position / self.angular_velocity

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

    def calculate_t_for_position(self, coordinates: list, save: bool = False) -> float:
        # TODO docstrings
        # TODO exceptions
        angular_position = self.coordinates_to_angle(coordinates)
        t = self.t_from_angular_position(angular_position)
        if save:
            self.known_date_s = t
        return t

    def calculate_orbit(self, period: float = None, from_known: bool = False) -> list:
        """
        Calculates all orbital coordinates
        :param from_known: bool
        :param period: float
        :return: orbit
        """
        # If no period is given, set period to self.period. Period is always in seconds
        if not period:
            period = self.period

        # Initialize two-dimensional list for orbit
        orbit = [[], []]

        # Generate a map of angular_positions for given period

        # Time interval is the amount of time that passes per t in seconds

        angular_pos = map(self.angular_position_at_t(from_known), range(int(period / self.time_interval) + 1))
        # For each angular position, generate x,y coordinates, append coordinates to orbit
        for angle in angular_pos:
            x, y = self.angular_position_to_coordinates(angle)
            orbit[0].append(x)
            orbit[1].append(y)
        self.orbit = orbit
        return orbit

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
