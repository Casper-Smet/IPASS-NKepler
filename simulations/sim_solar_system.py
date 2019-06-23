from lib.classes import Focus, Satellite
import matplotlib;

matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def animate(i):
    ax1.clear()
    ax1.set_ylim([axis_range * -1.1, axis_range * 1.1])
    ax1.set_xlim([axis_range * -1.1, axis_range * 1.1])

    ax1.scatter([0], [0], label=sun.name)
    for satellite in sun.satellite_list:
        ang_pos = lambda_dict[satellite.name](i)
        x, y = satellite.angular_position_to_coordinates(ang_pos)

        ax1.scatter(x, y, label=satellite.name)
        # ax1.plot([x, 0], [y, 0], label="{} Radius: {}".format(satellite.name, (x ** 2 + y ** 2) ** (1 / 2)))
        ax1.plot([x, 0], [y, 0], label="{} Radius".format(satellite.name))

    ax1.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
               fancybox=True, shadow=True, ncol=5)


def calculate_orbit_system(focus):
    satellites = focus.satellite_list
    for sat in satellites:
        # sat.time_interval = 1 * 60 * 60 * 24  # days recommended for inner planets
        sat.time_interval = 1 * 60 * 60 * 24 * 365 / 12  # months recommended for outer planets
        sat.calculate_velocity()
        sat.calculate_period()
        sat.calculate_angular_velocity()
        print(sat)

    lambda_dict = dict()

    for sat in satellites:
        lambda_dict[sat.name] = sat.angular_position_at_t()
        # sat.calculate_orbit(period)
        # sat.to_json("json/{}".format(sat.name))
    return lambda_dict


if __name__ == '__main__':
    sun = Focus("Sun", 1.989E30)

    # It is recommended to simulate mercury, venus, mars and earth separately from Jupiter, Saturn, Uranus and Neptune.
    # The latter being so much further from the sun that you cannot properly differentiate between the earlier planets.
    # The orbital periods of the latter also being substantially larger from the earlier (years instead of months)
    # mercury = Satellite("Mercury", 0.330E24, sun, 0.0579E12 + 2.440E6)
    # venus = Satellite("Venus", 4.87E24, sun, 0.1082E12 + 6.052E6)
    # earth = Satellite("Earth", 5.972E24, sun, 149600000000)
    # mars = Satellite("Mars", 0.642E24, sun, 0.228E12 + 3.390E6)

    jupiter = Satellite("Jupiter", 1900E24, sun, 0.7883E12 + 69.91E6)
    saturn = Satellite("Saturn", 568E24, sun, 1.427E12 + 58.2E6)
    uranus = Satellite("Uranus", 86.8E24, sun, 2.871E12 + 58.2E6)
    neptune = Satellite("Neptune", 102.4E24, sun, 4.498E12 + 24.6E6)

    lambda_dict = calculate_orbit_system(sun)

    periods = [x.period for x in sun.satellite_list]

    axis_range = sun.largest_radius()

    fig = plt.figure(figsize=(10, 6))
    ax1 = fig.add_subplot(1, 1, 1)
    box = ax1.get_position()
    ax1.set_position([box.x0 + box.width * 0.1, box.y0, box.width * 0.5, box.height / 6 * 5])

    ani = animation.FuncAnimation(fig, animate, interval=1, frames=int(max(periods) / jupiter.time_interval))

    # plt.show()

    # Uncomment the following line to save as GIF, make sure you've got imagemagick installed
    # ani.save("orbits/solarouter.gif", writer='imagemagick', fps=30)
