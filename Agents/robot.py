"""
Robot Rescue Challenge - Robot Class and Simulation Engine

This module provides the Robot class representing the rescue robot
that navigates the building layout.
"""

from enum import Enum
from typing import Set, Tuple, List, Optional
from dataclasses import dataclass
from grid import Grid, CellType, Position
import traceback


class Direction(Enum):
    """Cardinal directions for robot movement."""

    FORWARD = (0, -1)  # Up (decreasing y)
    BACKWARD = (0, 1)  # Down (increasing y)
    LEFT = (-1, 0)  # Left (decreasing x)
    RIGHT = (1, 0)  # Right (increasing x)


class RobotDestroyedException(Exception):
    """Exception raised when the robot is destroyed by fire."""

    pass


class MissionCompleteException(Exception):
    """Exception raised when the mission is completed successfully."""

    pass


@dataclass
class SimulationResult:
    """Result of a simulation run."""

    success: bool
    time_elapsed: int
    people_saved: int
    total_people: int
    message: str


class Robot:
    """
    The rescue robot that navigates the grid to save people.

    This class provides the interface that you will use to control the robot.
    """

    SCAN_TIME_COST = 10
    MOVE_TIME_COST = 1

    def __init__(self, grid: Grid):
        """
        Initialize the robot on the grid.

        Args:
            grid: The grid the robot operates on
        """
        self._grid = grid
        if grid.exit_position is None:
            raise ValueError("Grid must have an exit position")

        self._position = Position(grid.exit_position.x, grid.exit_position.y)
        self._carrying_person = False
        self._time_elapsed = 0
        self._people_saved = 0
        self._total_people = len(grid.person_positions)
    
    def print_grid(self):
        print(self._grid)

    @property
    def position(self) -> Position:
        """Get the current position of the robot."""
        return Position(self._position.x, self._position.y)

    @property
    def is_carrying_person(self) -> bool:
        """Check if the robot is currently carrying a person."""
        return self._carrying_person

    @property
    def time_elapsed(self) -> int:
        """Get the total time elapsed."""
        return self._time_elapsed

    @property
    def people_saved(self) -> int:
        """Get the number of people saved."""
        return self._people_saved

    def move(self, direction: Direction) -> bool:
        """
        Move the robot in the specified direction.

        Args:
            direction: The direction to move

        Returns:
            True if the move was successful, False if blocked
        """
        dx, dy = direction.value
        new_x = self._position.x + dx
        new_y = self._position.y + dy

        # Check bounds
        if not self._grid.is_valid_position(new_x, new_y):
            return False

        # Move takes time
        self._time_elapsed += self.MOVE_TIME_COST

        # Update position
        self._position = Position(new_x, new_y)

        # Check for fire
        if self._grid.get_cell(new_x, new_y) == CellType.FIRE:
            raise RobotDestroyedException("Robot was destroyed by fire")

        # Check for person (pickup)
        if (
            not self._carrying_person
            and self._grid.get_cell(new_x, new_y) == CellType.PERSON
        ):
            self._carrying_person = True
            self._grid.remove_person(self._position)

        # Check for exit (drop off) - mission complete!
        if self._carrying_person and self._position == self._grid.exit_position:
            self._carrying_person = False
            self._people_saved += 1
            raise MissionCompleteException("Person rescued successfully!")

        return True

    def sense_fires_around(self) -> int:
        """
        Sense the number of fires in cardinal direction cells (not diagonals).

        Returns:
            Number of fires in the 4 cardinal direction cells (up, down, left, right)
        """
        fire_count = 0
        cardinal_directions = [
            (0, -1),
            (0, 1),
            (-1, 0),
            (1, 0),
        ]  # up, down, left, right
        for dx, dy in cardinal_directions:
            check_x = self._position.x + dx
            check_y = self._position.y + dy
            if self._grid.is_valid_position(check_x, check_y):
                if self._grid.get_cell(check_x, check_y) == CellType.FIRE:
                    fire_count += 1
        return fire_count

    def scan_fires(self) -> Set[Position]:
        """
        Perform a scan to detect fire positions in adjacent cells.

        This is an expensive operation that takes 10 seconds.

        Returns:
            Set of fire positions in the 8 surrounding cells
        """
        self._time_elapsed += self.SCAN_TIME_COST
        fire_positions = set()
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                check_x = self._position.x + dx
                check_y = self._position.y + dy
                if self._grid.is_valid_position(check_x, check_y):
                    if self._grid.get_cell(check_x, check_y) == CellType.FIRE:
                        fire_positions.add(Position(check_x, check_y))
        return fire_positions

    def get_grid_dimensions(self) -> Tuple[int, int]:
        """
        Get the dimensions of the grid.

        Returns:
            Tuple of (width, height)
        """
        return (self._grid.width, self._grid.height)

    def get_exit_position(self) -> Position:
        """
        Get the position of the exit.

        Returns:
            Position of the exit cell
        """
        return Position(self._grid.exit_position.x, self._grid.exit_position.y)

    def get_person_position(self) -> Optional[Position]:
        """
        Get the position of the person to rescue.

        Returns:
            Position of the person, or None if already rescued
        """
        if self._grid.person_positions:
            person = next(iter(self._grid.person_positions))
            return Position(person.x, person.y)
        return None


def run_simulation(grid: Grid, solution_func) -> SimulationResult:
    """
    Run a simulation with the given grid and solution function.

    Args:
        grid: The grid to simulate on
        solution_func: A function that takes a Robot and controls it

    Returns:
        SimulationResult with the outcome
    """
    robot = Robot(grid)

    try:
        solution_func(robot)

        # If we get here, the solution ended without rescuing the person
        return SimulationResult(
            success=False,
            time_elapsed=robot.time_elapsed,
            people_saved=robot.people_saved,
            total_people=robot._total_people,
            message="Mission failed: Person was not rescued",
        )

    except MissionCompleteException:
        return SimulationResult(
            success=True,
            time_elapsed=robot.time_elapsed,
            people_saved=robot.people_saved,
            total_people=robot._total_people,
            message=f"Mission complete! Person saved in {robot.time_elapsed} seconds",
        )

    except RobotDestroyedException:
        return SimulationResult(
            success=False,
            time_elapsed=robot.time_elapsed,
            people_saved=robot.people_saved,
            total_people=robot._total_people,
            message="Robot was destroyed by fire",
        )

    except Exception as e:
        return SimulationResult(
            success=False,
            time_elapsed=robot.time_elapsed,
            people_saved=robot.people_saved,
            total_people=robot._total_people,
            message=f"Solution raised an exception: {str(e)}\n{traceback.format_exc()}",
        )
