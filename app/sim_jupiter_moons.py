from lib.classes import Focus, Satellite
import matplotlib;

matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib import style
import matplotlib.animation as animation


def animate(i):
    ax1.clear()
    ax1.set_ylim([axis_range * -1.1, axis_range * 1.1])
    ax1.set_xlim([axis_range * -1.1, axis_range * 1.1])

    ax1.scatter([0], [0], label=focus.name)
    for satellite in focus.satellite_list:
        ang_pos = lambda_dict[satellite.name](i)
        x, y = satellite.angular_displacement_to_coordinates(ang_pos)
        plt.plot(trail_dict[satellite.name][0], trail_dict[satellite.name][1])

        trail_dict[satellite.name][0].append(x)
        trail_dict[satellite.name][1].append(y)

        if len(trail_dict[satellite.name][0]) > trail_size:
            trail_dict[satellite.name][0].pop(0)
            trail_dict[satellite.name][1].pop(0)

        ax1.scatter(x, y, label=satellite.name)
        # ax1.plot([x, 0], [y, 0], label="{} Radius: {}".format(satellite.name, (x ** 2 + y ** 2) ** (1 / 2)))
        # ax1.plot([x, 0], [y, 0], label="{} Radius".format(satellite.name))

    ax1.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
               fancybox=True, shadow=True, ncol=5)


def calculate_orbit_system(focus):
    satellites = focus.satellite_list
    for sat in satellites:
        sat.time_interval = 1 * 60 * 60  # hours recommended
        sat.calculate_velocity()
        sat.calculate_period()
        sat.calculate_angular_velocity()
        print(sat)

    lambda_dict = dict()
    trail_dict = dict()

    for sat in satellites:
        lambda_dict[sat.name] = sat.angular_displacement_at_t()
        trail_dict[sat.name] = [[], []]
        # sat.calculate_orbit()  # Uncomment to calculate orbit
        # sat.to_json("json/{}".format(sat.name))  # Uncomment to save to JSON, add True to save orbit
    return lambda_dict, trail_dict


if __name__ == '__main__':
    focus = Focus("Jupiter", 1900E24)

    # This simulation file simulates the orbits of the 4 major moons around Jupiter.
    # Some of these moons have irregular orbits (E.G. Io), meaning that these orbits aren't very accurate to real life.
    # I would highly recommend reading up on Io and the effect tidal forces have on it, I find it to be both remarkably
    # interesting as humorous.
    # Lastly, no dates have been taken into account for the purposes of this simulation.

    io = Satellite("Io", 0.089E24, focus, 421.8E6 + 1.822E6)
    europa = Satellite("Europa", 0.048E24, focus, 670.9E6 + 1.568E6)
    ganymede = Satellite("Ganymede", 0.148E6, focus, 1070E6 + 2.631E6)
    callisto = Satellite("Callisto", 0.1076E24, focus, 1883E6 + 2.410E6)

    lambda_dict, trail_dict = calculate_orbit_system(focus)

    periods = [x.period for x in focus.satellite_list]

    axis_range = focus.largest_radius()

    trail_size = 20

    style.use('ggplot')

    fig = plt.figure(figsize=(10, 6))
    ax1 = fig.add_subplot(1, 1, 1)
    box = ax1.get_position()
    ax1.set_position([box.x0 + box.width * 0.1, box.y0, box.width * 0.5, box.height / 6 * 5])

    ani = animation.FuncAnimation(fig, animate, interval=1, frames=int(max(periods) / Satellite.time_interval))

    plt.show()

    # Uncomment the following line to save as GIF, make sure you've got imagemagick installed
    # ani.save("orbits/jupiter.gif", writer='imagemagick', fps=30)
