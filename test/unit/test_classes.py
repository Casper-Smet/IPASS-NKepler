import unittest
from datetime import datetime as dt
from lib.classes import Satellite, Focus
from lib.utility import time_difference


class TestSatellite(unittest.TestCase):

    def setUp(self) -> None:
        self.foc_1 = Focus("Earth", 5.972E24)
        self.sat_1 = Satellite("Moon", 7.34767309E22, self.foc_1, 384400E3)

        self.foc_2 = Focus("Sol", 1.989E30)
        self.sat_2 = Satellite("Mercury", 0.330E24, self.foc_2, 0.0579E12 + 2.440E6)
        self.sat_3 = Satellite("Venus", 4.87E24, self.foc_2, 0.1082E12 + 6.052E6)

        self.sat_1.calculate_velocity()
        self.sat_2.calculate_velocity()
        self.sat_3.calculate_velocity()

        self.sat_1.calculate_period()
        self.sat_2.calculate_period()
        self.sat_3.calculate_period()

        self.sat_1.calculate_angular_velocity()
        self.sat_2.calculate_angular_velocity()
        self.sat_3.calculate_angular_velocity()

        self.date1 = dt(2000, 5, 2)
        self.date2 = dt(2018, 6, 26)
        self.delta_t = time_difference(self.date1, self.date2)

    def tearDown(self) -> None:
        self.foc_1 = None
        self.sat_1 = None

        self.foc_2 = None
        self.sat_2 = None
        self.sat_3 = None

    def test_set_origin(self):
        self.sat_1.set_origin(self.date1, [383919600.095825, 19211992.66764875])
        self.assertEqual(self.sat_1.angular_displacement_to_coordinates(self.sat_1.angular_displacement_at_t(True)(0)),
                         (383919600.095825, 19211992.66764875))

        self.sat_2.set_origin(self.date1, (-50858319087.89675, -27678943937.716923))
        self.assertEqual(self.sat_2.angular_displacement_to_coordinates(self.sat_2.angular_displacement_at_t(True)(0)),
                         (-50858319087.89675, -27678943937.716923))

        self.sat_3.set_origin(self.date1, (108070822611.31126, 5408048589.019821))
        self.assertEqual(self.sat_3.angular_displacement_to_coordinates(self.sat_3.angular_displacement_at_t(True)(0)),
                         (108070822611.31126, 5408048589.019821))

    def test_update_origin(self):
        self.sat_1.set_origin(self.date1, [383919600.095825, 19211992.66764875])
        self.assertEqual(self.sat_1.angular_displacement_at_t(True)(self.delta_t), self.sat_1.update_origin(self.date2))

        self.sat_2.set_origin(self.date1, (-50858319087.89675, -27678943937.716923))
        self.assertEqual(self.sat_2.angular_displacement_at_t(True)(self.delta_t), self.sat_2.update_origin(self.date2))

        self.sat_3.set_origin(self.date1, (108070822611.31126, 5408048589.019821))
        self.assertEqual(self.sat_3.angular_displacement_at_t(True)(self.delta_t), self.sat_3.update_origin(self.date2))

    def test_calculate_velocity(self):
        self.assertAlmostEqual(self.sat_1.calculate_velocity(), 1018.27, places=2)
        self.assertAlmostEqual(self.sat_1.velocity, 1018.27, places=2)

        self.assertAlmostEqual(self.sat_2.calculate_velocity(), 47881.16, places=2)
        self.assertAlmostEqual(self.sat_2.velocity, 47881.16, places=2)

        self.assertAlmostEqual(self.sat_3.calculate_velocity(), 35025.74, places=2)
        self.assertAlmostEqual(self.sat_3.velocity, 35025.74, places=2)

    def test_calculate_period(self):
        self.assertAlmostEqual(self.sat_1.calculate_period(), 2371916.16, places=2)
        self.assertAlmostEqual(self.sat_1.period, 2371916.16, places=2)

        self.assertAlmostEqual(self.sat_2.calculate_period(), 7598223.61, places=2)
        self.assertAlmostEqual(self.sat_2.period, 7598223.61, places=2)

        self.assertAlmostEqual(self.sat_3.calculate_period(), 19410829.74, places=2)
        self.assertAlmostEqual(self.sat_3.period, 19410829.74, places=2)

    def test_calculate_angular_velocity(self):
        self.assertAlmostEqual(self.sat_1.calculate_angular_velocity() * 10 ** 10, 26489.91, places=2)
        self.assertAlmostEqual(self.sat_1.angular_velocity * 10 ** 10, 26489.91, places=2)

        self.assertAlmostEqual(self.sat_2.calculate_angular_velocity() * 10 ** 10, 8269.28, places=2)
        self.assertAlmostEqual(self.sat_2.angular_velocity * 10 ** 10, 8269.28, places=2)

        self.assertAlmostEqual(self.sat_3.calculate_angular_velocity() * 10 ** 10, 3236.95, places=2)
        self.assertAlmostEqual(self.sat_3.angular_velocity * 10 ** 10, 3236.95, places=2)

    def test_calculate_orbit(self):
        # TODO test orbit (too many values?) first last, 90 degree angles?
        pass

    def test_angle_to_y(self):
        self.assertAlmostEqual(self.sat_1.angle_to_y(1.0472), 332900635.872, places=2)

        self.assertAlmostEqual(self.sat_2.angle_to_y(6.2832), 850750.15, places=2)

        self.assertAlmostEqual(self.sat_3.angle_to_y(-2), -98391484650.57, places=2)

        with self.assertRaises(TypeError):
            self.sat_1.angle_to_y([])
            self.sat_2.angle_to_y(())
            self.sat_3.angle_to_y(1j)
            self.sat_1.angle_to_y("Test")

    def test_angle_to_x(self):
        self.assertAlmostEqual(self.sat_1.angle_to_x(1.0472), 192199184.79, places=2)

        self.assertAlmostEqual(self.sat_2.angle_to_x(6.2832), 57902439993.75, places=2)

        self.assertAlmostEqual(self.sat_3.angle_to_x(-2), -45029606235.06, places=2)

        with self.assertRaises(TypeError):
            self.sat_1.angle_to_x([])
            self.sat_2.angle_to_x(())
            self.sat_3.angle_to_x(1j)
            self.sat_1.angle_to_x("Test")

    def test_coordinates_to_angle(self):
        self.assertAlmostEqual(self.sat_1.coordinates_to_angle(self.sat_1.angular_displacement_to_coordinates(1.0472)),
                               1.0472, places=2)

        self.assertAlmostEqual(self.sat_2.coordinates_to_angle(self.sat_2.angular_displacement_to_coordinates(6.2832)),
                               1.4692819998884943e-05, places=7)

        self.assertAlmostEqual(self.sat_3.coordinates_to_angle(self.sat_3.angular_displacement_to_coordinates(-2)),
                               4.28,
                               places=2)

        with self.assertRaises(TypeError):
            self.sat_1.coordinates_to_angle(4)
            self.sat_2.coordinates_to_angle("Wow")
            self.sat_3.coordinates_to_angle(1.2)
            self.sat_3.coordinates_to_angle(1j)

    def test_angular_displacement_at_t(self):
        self.sat_1.angle_at_0 = 5.72
        self.assertAlmostEqual(self.sat_1.angular_displacement_at_t()(600), 5.72, places=2)
        self.assertAlmostEqual(self.sat_1.angular_displacement_at_t(True)(0), 5.72, places=2)

        self.sat_2.angle_at_0 = 1.57
        self.assertAlmostEqual(self.sat_2.angular_displacement_at_t()(8970), 1.57, places=2)
        self.assertAlmostEqual(self.sat_2.angular_displacement_at_t(True)(0), 1.57, places=2)

        self.sat_3.angle_at_0 = 0.03
        self.assertAlmostEqual(self.sat_3.angular_displacement_at_t()(23), 0.03, places=2)
        self.assertAlmostEqual(self.sat_3.angular_displacement_at_t(True)(0), 0.03, places=2)

    def test_angular_displacement_to_coordinates(self):
        x, y = self.sat_1.angular_displacement_to_coordinates(1.0472)
        self.assertAlmostEqual(x, 192199184.79, places=2)
        self.assertAlmostEqual(y, 332900635.872, places=2)

        x, y = self.sat_2.angular_displacement_to_coordinates(6.2832)
        self.assertAlmostEqual(x, 57902439993.75, places=2)
        self.assertAlmostEqual(y, 850750.15, places=2)

        x, y = self.sat_3.angular_displacement_to_coordinates(-2)
        self.assertAlmostEqual(x, -45029606235.06, places=2)
        self.assertAlmostEqual(y, -98391484650.57, places=2)

        with self.assertRaises(TypeError):
            self.sat_1.angular_displacement_to_coordinates([])
            self.sat_2.angular_displacement_to_coordinates(())
            self.sat_3.angular_displacement_to_coordinates(1j)
            self.sat_3.angular_displacement_to_coordinates("test")


class TestFocus(unittest.TestCase):
    def setUp(self) -> None:
        self.foc_1 = Focus("Sun", 1.989E30)

        self.sat_1 = Satellite("Mercury", 0.330E24, self.foc_1, 0.0579E12 + 2.440E6)
        self.sat_2 = Satellite("Venus", 4.87E24, self.foc_1, 0.1082E12 + 6.052E6)

        self.foc_2 = Focus("Jupyter", 1900E24)

        self.sat_3 = Satellite("Io", 0.089E24, self.foc_2, 421.8E6 + 1.822E6)
        self.sat_4 = Satellite("Europa", 0.048E24, self.foc_2, 670.9E6 + 1.568E6)
        self.sat_5 = Satellite("Ganymede", 0.148E6, self.foc_2, 1070E6 + 2.631E6)
        self.sat_6 = Satellite("Callisto", 0.1076E24, self.foc_2, 1883E6 + 2.410E6)

        self.sat_7 = Satellite("Test", 50)

    def tearDown(self) -> None:
        self.foc_1 = None

        self.sat_1 = None
        self.sat_2 = None

        self.foc_2 = None

        self.sat_3 = None
        self.sat_4 = None
        self.sat_5 = None
        self.sat_6 = None
        self.sat_7 = None
        self.sat_7 = None

    def test_add_to_satellites(self):
        satellites_foc_1 = self.foc_1.satellite_list.copy()
        self.foc_1.add_to_satellites(self.sat_7)
        self.assertEqual(self.foc_1.satellite_list[-1], self.sat_7)
        satellites_foc_1.append(self.sat_7)
        self.assertEqual(self.foc_1.satellite_list, satellites_foc_1)

        satellites_foc_2 = self.foc_2.satellite_list.copy()
        self.foc_2.add_to_satellites(self.sat_7)
        self.assertEqual(self.foc_2.satellite_list[-1], self.sat_7)
        satellites_foc_2.append(self.sat_7)
        self.assertEqual(self.foc_2.satellite_list, satellites_foc_2)

    def test_satellite_list(self):
        self.assertEqual(self.foc_1.satellite_list, [self.sat_1, self.sat_2])
        self.assertEqual(self.foc_2.satellite_list, [self.sat_3, self.sat_4, self.sat_5, self.sat_6])

    def test_largest_radius(self):
        self.assertEqual(self.foc_1.largest_radius(), max([self.sat_1.radius, self.sat_2.radius]))
        self.assertEqual(self.foc_2.largest_radius(),
                         max([self.sat_3.radius, self.sat_4.radius, self.sat_5.radius, self.sat_6.radius]))


if __name__ == '__main__':
    unittest.main()
