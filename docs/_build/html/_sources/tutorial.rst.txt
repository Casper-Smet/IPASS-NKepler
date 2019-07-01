NKepler tutorial
===============================
In this short tutorial, I will be explaining you the steps needed to calculate one orbital period using NKepler. I would
recommend looking at the simulation files in the app folder feature in the Github repository_.

Step 1: Import NKepler
----------------------

    from lib.classes import Satellite, Focus

Step 2: Initializing the two objects
------------------------------------
To calculate the orbit of a satellite, two objects are needed: a Focus and a Satellite. The Satellite is the object that
orbits, while the Focus is (usually) the static object around which the Satellite orbits. If you do not know the mass of
your satellite, you can enter 1 instead. It is only used when the satellite also functions as a Focus.

   sat1 = Satellite(name: str, mass: float)

   foc1 = Focus(name: str, mass: float)

In order to couple these objects, the following statement may be used:

    sat1.set_focus(foc1, radius: float)

Set_focus also adds sat1 to foc1's satellite_list, this way it is easier to access later!

Step 3: Calculating the necessary variables
-------------------------------------------
In order to calculate orbits, one needs a couple of variables:


- The satellite's velocity
- The satellite's period
- The satellite's angular velocity


These need to be calculated in order using the following lines of code:

    sat1.calculate_velocity()

    sat1.calculate_period()

    sat1.calculate_angular_velocity()

Step 4: (OPTIONAL) Setting time_interval
----------------------------------------
The variable time_interval is used to to decide how big the steps in t are. Their standard value is 3600, which equals 1
hour. If you want to calculate for different time intervals, run the following line of code:

    Satellite.time_interval = # Whatever value you want (1 = 1 sec, 60 = 1 min, 3600 = 1 hour, etc.)

Step 5: (OPTIONAL) Calculating angular displacement
---------------------------------------------------
The next step is to call the following function:

    ang_pos_lambda = sat1.angular_displacement_at_t()

This gets a lambda expression used to translate t (time) to angular displacement.
To then calculate angular displacement at t, simply enter the following line (do note that t is multiplied by
time_interval, do not t in seconds lest you set time_interval to 1:

    ang_pos = ang_pos_lambda(t)

Step 5: (OPTIONAL) Calculating X, Y coordinates
-----------------------------------------------
Then, you can calculate the x and y coordinates of the satellite using the following two lines:

    x = sat1.angle_to_x(ang_pos)

    y = sat1.angle_to_x(ang_pos)

Step 6: (OPTIONAL) Calculating X, Y coordinates, the smarter way!
-----------------------------------------------------------------
Instead of calling angle_to_x and angle_to_y separately, you can use the following line:

    x, y = sat1.angular_displacement_to_coordinates

Step 7: Calculating orbits, the smartest way!
---------------------------------------------
You can skip steps 4 through 6 by using the following line:

    orbit = sat1.calculate_orbit(period: optional)

This one function does everything steps 4 through 6 does for whatever period you would like. Here, the period can be
entered in seconds.


More features:
--------------
The workings of the other features aren't included in this tutorial. They can be understood through reading the
documentation and reading the sim files in the app folder. The latter can be found in the 'app' folder in Repository_.

.. _Repository: https://github.com/Casper-Smet/IPASS-NKepler