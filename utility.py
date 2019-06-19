gravitational_constant = 6.67408 * 10 ** (-11)  # m^3/kgs^2
pi = 3.14159265359
accuracy = 2


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


def range_setter(var, minimum, maximum):
    """Alters var to be within two given values, used in mean_anomaly()"""
    while var > maximum or var < minimum:
        if var < minimum:
            var += maximum
        else:
            var -= maximum
    return var
