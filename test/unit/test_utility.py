import unittest
from lib.utility import *


class TestUtility(unittest.TestCase):
    # Differences in the accuracy of the 'round' function can be attributed to the converter used to this these
    # functions only being accurate to that point.
    def test_degrees(self):
        self.assertEqual(round(degrees(6), 3), 343.775)
        self.assertEqual(round(degrees(2), 3), 114.592)
        self.assertEqual(round(degrees(60), 2), 3437.75)

        with self.assertRaises(TypeError):
            degrees("Test")
            degrees([])
            degrees(1j)
            degrees(())

    def test_radians(self):
        self.assertEqual(round(radians(60), 4), 1.0472)
        self.assertEqual(round(radians(360), 4), 6.2832)
        self.assertEqual(round(radians(-10), 4), -0.1745)

        with self.assertRaises(TypeError):
            radians("Test")
            radians([])
            radians(1j)
            radians(())

    def test_range_setter(self):
        self.assertEqual(range_setter(361, 360), 1)
        self.assertEqual(range_setter(50, 360), 50)
        self.assertEqual(range_setter(-100, 360), 260)

        with self.assertRaises(TypeError):
            range_setter("Test", 360)
            range_setter(10, "Test")
            range_setter("Test", "Test")
            range_setter([], 360)
            range_setter(360, [])
            range_setter([], [])

    def test_time_difference(self):
        self.assertEqual(time_difference(dt(2000, 5, 2), dt(2000, 5, 3)), 86400)

        with self.assertRaises(TypeError):
            time_difference([], 1j)
            time_difference(dt(200, 5, 2), "test")
            time_difference("2000-05-02", dt(2019, 6, 28))
            time_difference(1, 2.0)


if __name__ == '__main__':
    unittest.main()
