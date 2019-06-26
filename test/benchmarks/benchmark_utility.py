import cProfile
from lib.utility import *

if __name__ == '__main__':
    cp = cProfile.Profile()
    date1 = dt(2000, 5, 2)
    date2 = dt(2016, 6, 26)
    cp.enable()
    for i in range(500):
        range_setter(780, 360)
        radians(67)
        degrees(6)
        time_difference(date1, date2)
    cp.disable()
    cp.print_stats()
