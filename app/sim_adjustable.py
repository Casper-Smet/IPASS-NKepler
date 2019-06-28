from lib.classes import Focus, Satellite
import matplotlib;

matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
from matplotlib.widgets import Slider


def animate(i):
    ax1.clear()
    updater = False
    global mass_slider
    if mass_slider.val != earth.mass:
        updater = True
        earth.mass = float(mass_slider.val)
        print(f"Mass {earth.mass} kg")
    if radius_slider.val != moon.radius:
        updater = True
        moon.radius = float(radius_slider.val)
        print(f"Radius {moon.radius} m")
    if updater:
        moon.calculate_velocity()
        moon.calculate_period()
        moon.calculate_angular_velocity()

    ang_pos_lambda = moon.angular_displacement_at_t()

    ang_pos = ang_pos_lambda(i)
    borders = [-standard_radius * 3, standard_radius * 3]

    ax1.set_ylim(borders)
    ax1.set_xlim(borders)
    x, y = moon.angular_displacement_to_coordinates(ang_pos)
    ax1.scatter([0], [0])
    ax1.scatter(x, y)


if __name__ == '__main__':
    # This simulation file simulates an adjustable orbit for Luna (our moon) around the Earth. The two input variables,
    # mass of the focus and the radius of the orbit are adjustable using the two sliders in the bottom.
    # In this simulation file, the limitations of Matplotlib.Animation are shown. Changing the radius causes jittering
    # in the animation. Lastly, no dates are taken into account for the purposes of this simulation.

    earth = Focus("Earth", 5.972E24)
    moon = Satellite("Luna", 7.34767309E22)
    moon.time_interval = moon.time_interval * 24
    moon.set_focus(earth, 384400E3)
    moon.calculate_velocity()
    print(int(moon.calculate_period() / moon.time_interval))
    moon.calculate_angular_velocity()
    print(moon)

    standard_mass = earth.mass
    standard_radius = moon.radius

    style.use('ggplot')

    fig = plt.figure(figsize=(6, 6))
    ax1 = fig.add_subplot(1, 1, 1)

    ax_mass = plt.axes([0.25, .03, 0.50, 0.02])
    ax_radius = plt.axes([0.25, 0, 0.5, 0.02])

    mass_slider = Slider(ax_mass, "Mass", 0, standard_mass * 2, valinit=standard_mass)
    # Changing radius causing some jittering in the animation. This is a bug in matplotlib.animation, not NKepler
    radius_slider = Slider(ax_radius, "Radius", 0, standard_radius * 2, valinit=standard_radius)
    ani = animation.FuncAnimation(fig, animate, interval=1)
    plt.show()
