import cProfile
from lib.classes import *
import matplotlib.pyplot as plt
from datetime import datetime as dt


# Profiled per minute

def calculate_orbit_system(focus):
    satellites = focus.satellite_list
    for sat in satellites:
        sat.time_interval = 1 * 60  # minutes
        sat.calculate_velocity()
        sat.calculate_period()
        sat.calculate_angular_velocity()
        sat.calculate_orbit()
        sat.set_origin(date1, [sat.orbit[0][1000], sat.orbit[1][1000]])
        sat.calculate_orbit(from_known=True)
        sat.update_origin(date2)
        sat.calculate_orbit(from_known=True)


if __name__ == '__main__':
    cp = cProfile.Profile()
    cp.enable()
    sun = Focus("Sun", 1.989E30)
    mercury = Satellite("Mercury", 0.330E24, sun, 0.0579E12 + 2.440E6)
    venus = Satellite("Venus", 4.87E24, sun, 0.1082E12 + 6.052E6)
    earth = Satellite("Earth", 5.972E24, sun, 149600000000)
    mars = Satellite("Mars", 0.642E24, sun, 0.228E12 + 3.390E6)
    date1 = dt(2000, 5, 2)
    date2 = dt(2019, 6, 25)
    calculate_orbit_system(sun)
    cp.disable()
    print("Orbits calculated per minute, two full orbits per satellite")
    cp.print_stats()
    plt.show()
