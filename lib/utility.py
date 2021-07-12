from datetime import datetime as dt

gravitational_constant = 6.67408 * 10 ** (-11)  # m^3/kgs^2
G = gravitational_constant
pi = 3.14159265359


def degrees(angle: float) -> float:
    """Converts radians to degrees

    :param angle: float
    :return: angle in degrees
    :rtype: float
    """
    if type(angle) not in [int, float]:
        print("Please input correct type for angle")
        raise TypeError
    try:
        return angle * 180 / pi
    except Exception as e:
        print(e)
        return 0.0


def radians(angle: float) -> float:
    """Converts degrees to radians

    :param angle: float
    :return: angle in radians
    :rtype: float
    """
    if type(angle) not in [int, float]:
        raise TypeError
    try:
        return angle * pi / 180
    except Exception as e:
        print(e)
        return 0.0


def range_setter(var: float, maximum: float):
    """Alters var to 0 >= var <= maximum

    :param var: float
    :param maximum: float
    :return: var in range 0, maximum:
    :rtype: float
    """
    if type(var) not in [int, float]:
        print("Please input correct type for var")
        raise TypeError
    if type(maximum) not in [int, float]:
        print("Please input correct type for maximum")
        raise TypeError
    try:
        return var % maximum
    except Exception as e:
        print(e)
        return 0.0


def time_difference(date1: dt, date2: dt) -> float:
    """
    Calculates time_difference in seconds between date1 and date2.

    :param date1: datetime.datetime
    :param date2: datetime.datetime
    :return: time in seconds
    :rtype: float
    """
    if type(date1) != dt or type(date2) != dt:
        print("both date1 and date2 must be datetime.datetime objects")
        raise TypeError
    return (date2 - date1).total_seconds()
