import cProfile
from lib.classes import *
import matplotlib.pyplot as plt


# Profiled per day

def calculate_orbit_system(focus):
    satellites = focus.satellite_list
    for sat in satellites:
        sat.time_interval = 1 * 60   # hours recommended for inner planets
        sat.calculate_velocity()
        sat.calculate_period()
        sat.calculate_angular_velocity()
        sat.calculate_orbit()
        # plt.plot(sat.orbit[0], sat.orbit[1])

if __name__ == '__main__':
    cp = cProfile.Profile()
    cp.enable()
    sun = Focus("Sun", 1.989E30)
    mercury = Satellite("Mercury", 0.330E24, sun, 0.0579E12 + 2.440E6)
    venus = Satellite("Venus", 4.87E24, sun, 0.1082E12 + 6.052E6)
    earth = Satellite("Earth", 5.972E24, sun, 149600000000)
    mars = Satellite("Mars", 0.642E24, sun, 0.228E12 + 3.390E6)
    calculate_orbit_system(sun)
    cp.disable()
    print("Orbits calculated per hour, one full orbit per satellite")
    cp.print_stats()
    plt.show()
