import unittest
from lib.classes import Satellite, Focus


# TODO test angular_velocity (too small?)
# TODO test orbit (too many values?)
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

    def tearDown(self) -> None:
        self.foc_1 = None
        self.sat_1 = None

        self.foc_2 = None
        self.sat_2 = None
        self.sat_3 = None

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
