gravitational_constant = 6.67408 * 10 ** (-11)  # m^3/kgs^2
pi = 3.14159265359


def degrees(angle):
    """Converts radians to degrees"""
    try:
        return angle * 180 / pi
    except Exception as e:
        print(e)


def radians(angle):
    """Converts degrees to radians"""
    try:
        return angle * pi / 180
    except Exception as e:
        print(e)

