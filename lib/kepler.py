from math import sin, cos, radians, sqrt
from lib.utility import range_setter


# Todo decide on removal
# Todo Add exceptions
# Todo Add returns to docstrings

def sin_r(angle):
    return sin(radians(angle))


def cos_r(angle):
    return cos(radians(angle))


def mean_anomaly(d, n, L, P):
    """Calculates the mean anomaly of an orbit using the following variables:
    d <-- days since epoch
    n <-- daily motion (revolutions per day)
    L <-- mean longitude
    P <-- longitude of the perihelion"""

    M = n * d + L - P

    M = range_setter(M, 360)

    return M


def radius_vector(a, e, v):
    """The distance from the planet to the focus of the ellipse; radius vector:
    r <-- radius vector
    a <-- semi-major axis
    e <-- eccentricity
    v <-- true anomaly"""

    r = a * (1 - e ** 2) / (1 + e * cos(v))

    return r


def heliocentric(r, v, o, p, i):
    """Calculate the heliocentric coordinates, returns tuple X, Y, Z
    r <-- radius vector
    v <-- true anomaly
    o <-- longitude of ascending node
    p <-- longitude of perihelion
    i <-- inclination of plane of orbit"""
    # v = radians(v)
    # p = radians(p)
    # o = radians(o)
    # i = radians(i)
    vpo = v + p - o
    vpo = range_setter(vpo, 0, 360)
    # print(cos_r(o) * cos_r(vpo), - (sin_r(o) * sin_r(vpo) * cos_r(i)))
    X = r * (cos_r(o) * cos_r(vpo) - sin_r(o) * sin_r(vpo) * cos_r(i))
    Y = r * (sin_r(o) * cos_r(vpo) + cos_r(o) * sin_r(vpo) * cos_r(i))
    Z = r * (sin_r(vpo) * sin_r(i))
    return X, Y, Z


def find_d(dele):
    """Lambda for days since day number. The day you know L and P for."""
    return lambda dpos: dpos - dele


def main():
    d_mars = -60  # 0h 21st June 1997
    n_mars = 0.5240613
    L_mars = 262.42784
    P_mars = 336.0882
    M_mars = mean_anomaly(d_mars, n_mars, L_mars, P_mars)
    e_mars = 0.0934231
    a_mars = 1.5236365
    v_mars = 244.921657

    r_mars = radius_vector(a_mars, e_mars, radians(v_mars))
    o_mars = 49.5664
    i_mars = 1.84992

    coords_mars = heliocentric(r_mars, v_mars, o_mars, P_mars, i_mars)
    print(coords_mars)
    r_check = int()
    for i in coords_mars:
        r_check = r_check + i ** 2

    print(sqrt(r_check), r_mars)


if __name__ == '__main__':
    main()
