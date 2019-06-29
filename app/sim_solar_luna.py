from lib.classes import Focus, Satellite
import matplotlib;

matplotlib.use("TkAgg")
from matplotlib import style
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def animate(i):
    ax1.clear()

    ax1.set_ylim((earth.radius * - 1.2, earth.radius * 1.2))
    ax1.set_xlim((earth.radius * - 1.2, earth.radius * 1.2))

    ax1.scatter([0], [0], label="Sun")
    ax1.plot(earth.orbit[0][:i], earth.orbit[1][:i], label="Earth")
    ax1.plot(moon_orbit[0][:i], moon_orbit[1][:i], label="Moon")
    ax1.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
               fancybox=True, shadow=True, ncol=5)


def calculate_orbit_system(focus):
    satellites = focus.satellite_list
    for sat in satellites:
        sat.calculate_velocity()
        sat.calculate_period()
        sat.calculate_angular_velocity()
        calculate_orbit_system(sat)
        print(sat)


if __name__ == '__main__':
    sun = Focus("Sun", 1.989E30)

    # This simulation file simulates the orbit of Luna (our moon) around the earth, as the earth orbits the sun
    # This is circa 365 days. For the purposes of this simulation, Earth's mass has been multiplied by 10^4 and the
    # radius between the moon and the earth multiplied by 10. This was done to make it easier to differentiate between
    # earth and the moon.

    earth = Satellite("Earth", 5.972E28, sun, 149600000000)
    moon = Satellite("Luna", 7.34767309E22, earth, 384400E4)
    print(earth.satellite_list)

    Satellite.time_interval = 1 * 60 * 60 * 24  # days recommended.

    calculate_orbit_system(sun)

    trail_size = 3000

    style.use('ggplot')
    earth.calculate_orbit()
    moon.calculate_orbit(earth.period)
    moon_orbit = moon.absolute_orbit_conversion()

    fig = plt.figure(figsize=(10, 6))
    ax1 = fig.add_subplot(1, 1, 1)
    box = ax1.get_position()
    ax1.set_position([box.x0 + box.width * 0.1, box.y0, box.width * 0.5, box.height / 6 * 5])
    #
    ani = animation.FuncAnimation(fig, animate, interval=1, frames=int(earth.period / Satellite.time_interval + 1))

    plt.show()

    # Uncomment the following line to save as GIF, make sure you've got imagemagick installed
    # ani.save("orbits/solarluna.gif", writer='imagemagick', fps=60)
