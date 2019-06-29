from math import cos, sin, atan2
from lib.utility import gravitational_constant, pi, range_setter, time_difference
from datetime import datetime as dt
import json
from functools import lru_cache


class Focus:
    """Object around which satellite will  orbit"""
    name: str
    mass: float
    radius: float
    satellite_list: list

    # TODO Remove radius from Focus

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
    middle_point: list
    # Calculated variables
    velocity: float
    period: float
    angular_velocity: float

    # Date related variables
    known_date: dt

    accuracy: int = 2
    time_interval: int = 1 * 60 * 60  # step size for t in seconds. Base position is 3600 (1 hour)

    satellite_list: list

    # # Only saved when Satellite has a satellite of its own, use middle_point?
    # x, y = 0.0, 0.0

    def __init__(self, name: str, mass: float, focus: Focus = None, radius: float = None, velocity: float = None,
                 period: float = None, angular_velocity: float = None,
                 known_date_dt: dt = None, orbit: tuple = ([], [])):
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
        # TODO EXCEPTIONS (including negative mass and radius)
        # TODO add variables to Docstring
        # TODO add possibility of sub-satellites.
        try:
            # Independent of focus
            self.name = name
            self.mass = mass
            # Dependent on focus
            self.focus = focus
            if focus:
                focus.add_to_satellites(self)
            self.middle_point = [0, 0]
            self.radius = radius
            #     Calculated from focus
            self.velocity = velocity
            self.period = period
            #     Calculated from velocity and radius
            self.angular_velocity = angular_velocity
            #     Calculated from angular velocity and radius
            self.orbit = orbit
            # Date related variables
            self.known_date = known_date_dt
            self.angle_at_0 = 0.0

            # For sub satellites:
            self.satellite_list = list()

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

    def add_to_satellites(self, satellite: object):
        """
        Adds satellite to satellite_list
        :param satellite:
        """
        if type(satellite) != Satellite:
            raise TypeError

        self.satellite_list.append(satellite)

    def set_origin(self, known_date_dt: dt, coordinates: list):
        """
        Set an origin point for the Satellite's orbit. The known date is set to equal a relative value of t in seconds.
        This value of t is the first moment the Satellite has reached those coordinates in one orbit.
        :param known_date_dt: datetime
        :param coordinates: list
        """
        # TODO rewrite docstring
        if type(known_date_dt) != dt:
            raise TypeError
        if type(coordinates) not in [list, tuple]:
            raise TypeError
        if len(coordinates) != 2:
            raise ValueError
        if type(coordinates[0]) not in [int, float] or type(coordinates[1]) not in [int, float]:
            raise TypeError

        self.known_date = known_date_dt
        self.angle_at_0 = self.coordinates_to_angle(coordinates)
        print(f"{self.known_date} equals {self.angle_at_0}")

    def update_origin(self, updated_date: dt) -> float:
        """
        Updates origin point for the satellite's orbit. Accepts a datetime object, then calculates the difference in
        time between the entered date and known_date. Next it calculates the angular displacement for that difference
        in time. Angle_at_0 is set to that angular displacement, known_date is set to the updated_date.
        :param updated_date: datetime
        :return angle_at_0: float
        """
        # TODO rename?, add option to save/not save
        if type(updated_date) != dt:
            raise TypeError

        time = time_difference(self.known_date, updated_date)
        new_angle = self.angular_displacement_at_t(True)(time)

        self.angle_at_0 = new_angle
        self.known_date = updated_date
        print(f"{self.known_date} equals {self.angle_at_0}")
        return self.angle_at_0

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
        """
        Calculates angular displacement with coordinates of the satellite and its focus using the following formula:
        O = atan2(dy, dx)
        :param coordinates:
        :return angular displacement:
        """
        if type(coordinates) not in [list, tuple]:
            raise TypeError
        return range_setter(atan2(coordinates[1] - self.middle_point[1], coordinates[0] - self.middle_point[0]),
                            6.283185307180001)

    def angular_displacement_at_t(self, from_known: bool = False):
        """
        Returns lambda that calculates angular position at time index t.
        O(t) = wt + theta0
        or
        O(t) = wt
        """

        # Time interval is the amount of time that passes per t in seconds
        if from_known:
            return lambda t: round(
                range_setter(self.angular_velocity * (t * self.time_interval) + self.angle_at_0, 6.283185307180001),
                self.accuracy)
        else:
            return lambda t: round(
                range_setter(self.angular_velocity * t * self.time_interval, 6.283185307180001), self.accuracy)

    @lru_cache(maxsize=None)
    def angular_displacement_to_coordinates(self, angular_displacement: float) -> tuple:
        """
        Calculates X,Y coordinates with angular position. Calls angle_to_y and angle_to_x
        :return: x,y
        :param angular_displacement:
        :rtype: tuple
        """
        x = self.angle_to_x(angular_displacement)
        y = self.angle_to_y(angular_displacement)
        return x, y

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

        # Generate a map of angular_displacements for given period

        # Time interval is the amount of time that passes per t in seconds

        angular_pos = map(self.angular_displacement_at_t(from_known), range(int(period / self.time_interval) + 1))
        # For each angular position, generate x,y coordinates, append coordinates to orbit
        for angle in angular_pos:
            x, y = self.angular_displacement_to_coordinates(angle)
            orbit[0].append(x)
            orbit[1].append(y)
        self.orbit = orbit
        return orbit

    def absolute_orbit_conversion(self):
        # TODO Test
        # TODO docstrings
        if type(self.focus) != Satellite:
            print("absolute_orbit_conversion requires a satellite focus.")
            raise TypeError
        if len(self.focus.orbit[0]) < len(self.orbit[0]):
            print("absolute_orbit_conversion requires a calculated orbit of the same length or greater than the sub "
                  "satellite")
            raise ValueError
        focus_orbit = self.focus.orbit
        satellite_orbit = self.orbit
        absolute_orbit = [[], []]
        for t in range(len(focus_orbit[0])):
            absolute_orbit[0].append(satellite_orbit[0][t] + focus_orbit[0][t])
            absolute_orbit[1].append(satellite_orbit[1][t] + focus_orbit[1][t])

        return absolute_orbit

    def absolute_position_at_t(self, t: float, from_known: bool = False) -> tuple:
        # TODO docstring
        # TODO testing
        if type(self.focus) != Satellite:
            print("absolute_position_at_t requires a satellite focus.")
            raise TypeError
        # Calculate angular displacement for both focus and satellite
        satellite_angular_displacement = self.angular_displacement_at_t(from_known)(t)
        focus_angular_displacement = self.focus.angular_displacement_at_t(from_known)(t)

        satellite_relative_pos = self.angular_displacement_to_coordinates(satellite_angular_displacement)
        focus_relative_pos = self.focus.angular_displacement_to_coordinates(focus_angular_displacement)

        absolute_x = satellite_relative_pos[0] + focus_relative_pos[0]
        absolute_y = satellite_relative_pos[1] + focus_relative_pos[1]

        return absolute_x, absolute_y

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
