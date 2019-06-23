gravitational_constant = 6.67408 * 10 ** (-11)  # m^3/kgs^2
pi = 3.14159265359


def degrees(angle: float) -> float:
    """Converts radians to degrees
    :rtype: float
    :param angle: float
    :return angle in degrees: float
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
    :rtype: float
    :param angle: float
    :return angle in radians: float
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
    :param maximum: float
    :return: float
    :type var: float
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
