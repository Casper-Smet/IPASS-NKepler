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


if __name__ == '__main__':
    unittest.main()
