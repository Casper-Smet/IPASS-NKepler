from lib.classes import Focus, Satellite
from datetime import datetime as dt
import matplotlib;

matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib import style
import matplotlib.animation as animation


def animate(i):
    ax1.clear()
    ax1.set_ylim([axis_range * -1.1, axis_range * 1.1])
    ax1.set_xlim([axis_range * -1.1, axis_range * 1.1])
    ax1.scatter(scatter_able_pos0[0], scatter_able_pos0[1], label='Date set at lines 60-63')
    ax1.scatter(scatter_able_updated_pos0[0], scatter_able_updated_pos0[1], label='2019-7-3')

    ax1.scatter([0], [0], label=focus.name)
    for satellite in focus.satellite_list:
        ax1.plot(satellite.orbit[0][:i], satellite.orbit[1][:i], label=satellite.name)

    ax1.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
               fancybox=True, shadow=True, ncol=5)


def calculate_orbit_system(focus):
    satellites = focus.satellite_list
    for sat in satellites:
        sat.calculate_velocity()
        sat.calculate_period()
        sat.calculate_angular_velocity()
        print(sat)
        # sat.calculate_orbit()  # Uncomment to calculate orbit
        # sat.to_json("json/date-{}".format(sat.name))  # Uncomment to save to JSON, add True to save orbit


if __name__ == '__main__':
    focus = Focus("Jupiter", 1900E24)

    # This simulation file simulates the orbits of the 4 major moons around Jupiter, and shows positions based on dates.
    # The origin functions are by far the hardest to visualise. In the following plot, the red dots equal the positions
    # entered at lines 60 through 63. The blue dots are the coordinates at 2019-7-3, set in the for loop at line 73.
    # Finally, all lines start at blue dots.

    Satellite.time_interval = 1 * 60 * 60  # hours recommended

    io = Satellite("Io", 0.089E24, focus, 421.8E6 + 1.822E6)
    europa = Satellite("Europa", 0.048E24, focus, 670.9E6 + 1.568E6)
    ganymede = Satellite("Ganymede", 0.148E6, focus, 1070E6 + 2.631E6)
    callisto = Satellite("Callisto", 0.1076E24, focus, 1883E6 + 2.410E6)

    calculate_orbit_system(focus)

    periods = [x.period for x in focus.satellite_list]

    axis_range = focus.largest_radius()

    # Set origins of all planets to different dates, set_origin calculates an angular displacement offset for use in
    # angular displacement at t(True)
    io.set_origin(dt(2000, 5, 2), [42627274.42883879, 421471842.9014784])
    europa.set_origin(dt(2012, 6, 23), [-401165171.057527, 539703359.7768177])
    ganymede.set_origin(dt(2016, 10, 14), [-935297659.4145851, 525124319.0470223])
    callisto.set_origin(dt(2019, 6, 28), [-874635796.2695737, -1670264377.8707278])

    # Make a list containing all starting positions based on their origin date
    pos0_list = list(map(lambda x: x.angular_displacement_to_coordinates(x.angular_displacement_at_t(True)(0)),
                         focus.satellite_list))

    scatter_able_pos0 = list(zip(*pos0_list))

    # Set origin date to 2019-7-3, update_origin calculates an angular displacement offset for use in angular
    # displacement at t(true)
    for sat in focus.satellite_list:
        sat.update_origin(dt(2019, 7, 3))
        sat.calculate_orbit(from_known=True)

    updated_pos0_list = list(map(lambda x: x.angular_displacement_to_coordinates(x.angular_displacement_at_t(True)(0)),
                                 focus.satellite_list))

    scatter_able_updated_pos0 = list(zip(*updated_pos0_list))
    style.use('ggplot')

    fig = plt.figure(figsize=(10, 6))
    ax1 = fig.add_subplot(1, 1, 1)
    box = ax1.get_position()
    ax1.set_position([box.x0 + box.width * 0.1, box.y0, box.width * 0.5, box.height / 6 * 5])

    ani = animation.FuncAnimation(fig, animate, interval=1, frames=int(max(periods) / Satellite.time_interval))

    plt.show()

    # Uncomment the following line to save as GIF, make sure you've got imagemagick installed
    # ani.save("orbits/jupiterdate.gif", writer='imagemagick', fps=30)
