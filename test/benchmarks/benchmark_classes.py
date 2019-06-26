import cProfile
from lib.classes import *
import matplotlib.pyplot as plt
# TODO add origin functions

# Profiled per day

def calculate_orbit_system(focus):
    satellites = focus.satellite_list
    for sat in satellites:
        sat.time_interval = 1 * 60   # minutes
        sat.calculate_velocity()
        sat.calculate_period()
        sat.calculate_angular_velocity()
        sat.calculate_orbit()
        for i in range(10, 100):
            sat.calculate_t_for_position([sat.orbit[0][i], sat.orbit[1][i]])

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
    print("Orbits calculated per minute, one full orbit per satellite")
    cp.print_stats()
    plt.show()
