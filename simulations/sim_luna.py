from lib.classes import Focus, Satellite
import matplotlib;

matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def animate(i):
    # print(i)
    ax1.clear()

    ax1.set_ylim([min(orbit[0]) * 3, max(orbit[0]) * 3])
    ax1.set_xlim([min(orbit[1]) * 3, max(orbit[1]) * 3])

    ax1.set_title("Moon orbiting around the earth, m h^-1, roughly 27 days")

    ax1.scatter([0], [0], label='Earth')

    x = orbit[0][i]
    y = orbit[1][i]

    ax1.plot(orbit[1], orbit[0], label='Orbit {} m '.format(moon.velocity * moon.period))
    ax1.plot([x, 0], [y, 0], label='Radius {} m'.format(round((x ** 2 + y ** 2) ** 1 / 2), 2))

    ax1.scatter(x, y, label='Moon')
    ax1.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
               fancybox=True, shadow=True, ncol=5)


if __name__ == '__main__':
    # Code to generate orbits, uncomment this block to calculate it yourself:
    earth = Focus("Earth", 5.972E24)
    moon = Satellite("Luna", 7.34767309E22)
    moon.time_interval = moon.time_interval * 24
    moon.set_focus(earth, 384400E3)
    moon.calculate_velocity()
    print(int(moon.calculate_period() / moon.time_interval))
    moon.calculate_angular_velocity()
    print(moon)
    # A gap shows up if you calculate per day, to avoid this the the moon is plotted over twice its period.
    orbit = moon.calculate_orbit(moon.period * 2)
    moon.to_json('json/Luna')

    # If you are calculating the orbits yourself, comment the 4 following lines
    # For per day:
    # moon, foc1 = json_satellite_construct('json/Luna')

    # For per hour:
    # moon, foc1, = json_satellite_construct('json/moon-hours')

    orbit = moon.orbit

    fig = plt.figure(figsize=(10, 6))
    ax1 = fig.add_subplot(1, 1, 1)
    ax1.set_ylim([min(orbit[0]) * 3, max(orbit[0]) * 3])
    ax1.set_xlim([min(orbit[1]) * 3, max(orbit[1]) * 3])
    box = ax1.get_position()
    ax1.set_position([box.x0 + box.width * 0.1, box.y0, box.width * 0.5, box.height / 6 * 5])
    ax1.scatter(orbit[1], orbit[0])
    ani = animation.FuncAnimation(fig, animate, interval=1, frames=len(orbit[0]))

    plt.show()
    # Uncomment the following line to save as GIF, make sure you've got imagemagick installed
    # ani.save("orbits/moon.gif", writer='imagemagick', fps=30)
