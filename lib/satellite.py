from dataclasses import Field, dataclass, field
from functools import lru_cache
from typing import List, Union

import numpy as np

from utility import G


@dataclass
class Focus():
    name: str
    mass: int = 1
    x: int = 0
    y: int = 0
    satellite_list: List["Satellite"] = field(default_factory=list)
    ...


@dataclass
class Satellite(Focus):
    """Satellite that will orbit."""

    # Variables dependent on Focus
    focus: Focus = None
    radius: float = None
    # Calculated variables
    velocity: float = None
    period: float = None
    angular_velocity: float = None

    # # Date related variables
    # known_date: dt
    angle_at_0: float = 0.

    accuracy: int = 2
    # step size for t in seconds. Base position is 3600 (1 hour)
    time_interval: int = 1 * 60 * 60

    def __post_init__(self) -> None:
        """Adds self to focus' satellite_list."""
        if self.focus is None:
            return
        if self.radius is None:
            raise ValueError("Radius must not be None if focus is passed.")
        self.focus.satellite_list.append(self)

        self.calculate_velocity()
        self.calculate_period()
        self.calculate_angular_velocity()

    def calculate_velocity(self) -> float:
        """Calculates velocity of a satellite in orbit.

        v = sqrt((G * M) / r)

        Returns:
            float: velocity
        """

        self.velocity = np.sqrt((G * self.focus.mass) / self.radius)
        return self.velocity

    def calculate_period(self) -> float:
        """Calculates the period of the satellite (in seconds).

        T = (2 * pi * r) / v

        Returns:
            float: period
        """
        self.period = (2 * np.pi * self.radius) / self.velocity
        return self.period

    def calculate_angular_velocity(self) -> float:
        """Calculates the angular velocity of the satellite rad/ T^-1.

        w = v / r

        Returns:
            float: Angular velocity
        """
        self.angular_velocity = self.velocity / self.radius
        return self.angular_velocity

    def angular_displacement_at_t(self, t: np.ndarray) -> np.ndarray:
        return (self.angular_velocity * self.time_interval * t) % 6.283185307180001

    def angle_to_x(self, angles: np.ndarray) -> np.ndarray:
        return np.cos(angles) * self.radius

    def angle_to_y(self, angles: np.ndarray) -> np.ndarray:
        return np.sin(angles) * self.radius

    # @lru_cache(maxsize=None)
    def angular_displacement_to_coordinates(self, angular_displacement: np.ndarray) -> np.ndarray:
        """
        Calculates X,Y coordinates with angular position. Calls angle_to_y and angle_to_x

        :return: x,y
        :param angular_displacement:
        :rtype: tuple
        """
        x = self.angle_to_x(angular_displacement)
        y = self.angle_to_y(angular_displacement)
        return np.vstack((x, y))

    def calculate_orbit(self, period: float = None, from_known: bool = False) -> np.ndarray:
        period = self.period if period is None else period
        time_steps = int(period / self.time_interval)
        angular_poss = self.angular_displacement_at_t(np.arange(time_steps))
        self.orbit = self.angular_displacement_to_coordinates(angular_poss)
        return self.orbit


def main() -> None:
    sun = Focus("Sun", mass=int(1.989E30))
    earth = Satellite("Earth", mass=int(5.972E24), focus=sun, radius=int(384400E3))
    print(earth)
    print(earth.calculate_orbit(earth.period * 365))


if __name__ == "__main__":
    main()
