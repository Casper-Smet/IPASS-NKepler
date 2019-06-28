from lib.classes import Focus, Satellite
import matplotlib;

matplotlib.use("TkAgg")
from matplotlib import style
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def animate(i):
    ax1.clear()
    ax1.set_ylim([axis_range * -1.1, axis_range * 1.1])
    ax1.set_xlim([axis_range * -1.1, axis_range * 1.1])

    ax1.scatter([0], [0], label=sun.name)
    for satellite in sun.satellite_list:
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
        ax1.plot([x, 0], [y, 0], label="{} Radius".format(satellite.name))

    ax1.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
               fancybox=True, shadow=True, ncol=5)


def calculate_orbit_system(focus):
    satellites = focus.satellite_list
    for sat in satellites:
        sat.calculate_velocity()
        sat.calculate_period()
        sat.calculate_angular_velocity()
        print(sat)

    lambda_dict = dict()
    trail_dict = dict()

    for sat in satellites:
        lambda_dict[sat.name] = sat.angular_displacement_at_t()
        trail_dict[sat.name] = [[], []]
        # sat.calculate_orbit(period)  # Uncomment to calculate period
        # sat.to_json("json/{}".format(sat.name))  # Uncomment to save to JSON, add True to save orbit
    return lambda_dict, trail_dict


if __name__ == '__main__':
    sun = Focus("Sun", 1.989E30)

    # This is a simulation file for the inner four planets of our solar system. Mercury and Mars have more elliptically
    # shaped orbits than Earth and Venus. Mercury and Mars' orbits are thus less accurate than Earth and Venus'.
    # Lastly, no dates are taken into account for the purposes of this simulation.
    mercury = Satellite("Mercury", 0.330E24, sun, 0.0579E12 + 2.440E6)
    venus = Satellite("Venus", 4.87E24, sun, 0.1082E12 + 6.052E6)
    earth = Satellite("Earth", 5.972E24, sun, 149600000000)
    mars = Satellite("Mars", 0.642E24, sun, 0.228E12 + 3.390E6)

    Satellite.time_interval = 1 * 60 * 60 * 24  # days recommended for inner planets

    lambda_dict, trail_dict = calculate_orbit_system(sun)

    periods = [x.period for x in sun.satellite_list]

    axis_range = sun.largest_radius()

    trail_size = 20

    style.use('ggplot')

    fig = plt.figure(figsize=(10, 6))
    ax1 = fig.add_subplot(1, 1, 1)
    box = ax1.get_position()
    ax1.set_position([box.x0 + box.width * 0.1, box.y0, box.width * 0.5, box.height / 6 * 5])

    ani = animation.FuncAnimation(fig, animate, interval=1, frames=int(max(periods) / Satellite.time_interval))

    plt.show()

    # Uncomment the following line to save as GIF, make sure you've got imagemagick installed
    # ani.save("orbits/solarinner.gif", writer='imagemagick', fps=30)
