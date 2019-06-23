import cProfile
from lib.utility import *

if __name__ == '__main__':
    cp = cProfile.Profile()
    cp.enable()
    for i in range(500):
        range_setter(780, 360)
        radians(67)
        degrees(6)
    cp.disable()
    cp.print_stats()
