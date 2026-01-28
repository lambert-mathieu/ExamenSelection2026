from robot import Robot, Direction, Position
from enum import Enum
from typing import List

class Tile(Enum):
    UNKNOWN = 1
    EMPTY = 2
    POTENTIAL_FIRE = 3
    FIRE = 4

CARDINAL_DIRECTIONS = [
    Position(0, -1),
    Position(0, 1),
    Position(-1, 0),
    Position(1, 0),
]

class Direction(Enum):
    RIGHT = Position(1, 0)
    LEFT = Position(-1, 0)
    DOWN = Position(0, 1)
    UP = Position(0, -1)

class CustomMap:
    def __init__(self, width: int, height: int, target_pos: Position, starting_pos: Position):
        self.width = width
        self.height = height
        self.tiles: List[List[Tile]] = [
            [Tile.UNKNOWN for _ in range(width)] for _ in range(height)
        ]
        self.pos = starting_pos
        self.target_pos = target_pos
        self.starting_pos = starting_pos
        self.set_tile(target_pos.x, target_pos.y, Tile.EMPTY)
        self.set_tile(starting_pos.x, starting_pos.y, Tile.EMPTY)

    def set_tile(self, x: int, y: int, tile: Tile) -> None:
        if self.is_valid_position(x, y):
            self.tiles[y][x] = tile

    def get_tile(self, x: int, y: int) -> Tile:
        if self.is_valid_position(x, y):
            return self.tiles[y][x]
        return None

    def is_valid_position(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height
    
    def tileToString(self, tile: Tile):
        if tile == Tile.UNKNOWN: return "."
        if tile == Tile.EMPTY: return "O"
        if tile == Tile.POTENTIAL_FIRE: return "!"
        if tile == Tile.FIRE: return "F"
    
    def get_close_count(self, tiles: List[Tile]):
        count = 0
        for direction in CARDINAL_DIRECTIONS:
            target_x = self.pos.x + direction.x
            target_y = self.pos.y + direction.y
            tile = self.get_tile(target_x, target_y)
            if (tile in tiles):
                count += 1
        return count
    
    def set_tiles_arround(self, tiles: List[Tile], tile: Tile):
        for direction in CARDINAL_DIRECTIONS:
            target_x = self.pos.x + direction.x
            target_y = self.pos.y + direction.y
            if self.get_tile(target_x, target_y) in tiles:
                self.set_tile(target_x, target_y, tile)
    
    def detect_best_direction(self):
        ideal_directions = self.detect_ideal_directions_order()
        if (ideal_directions):
    
    def detect_ideal_directions_order(self):
        deltaX = self.target_pos.x - self.pos.x
        deltaY = self.target_pos.y - self.pos.y
        if abs(deltaX) > abs(deltaY):
            if deltaX > 0:
                if deltaY > 0:
                    return [Direction.RIGHT, Direction.DOWN, Direction.UP, Direction.LEFT]
                else:
                    return [Direction.RIGHT, Direction.UP, Direction.DOWN, Direction.LEFT]
            else:
                if deltaY > 0:
                    return [Direction.LEFT, Direction.DOWN, Direction.UP, Direction.RIGHT]
                else:
                    return [Direction.LEFT, Direction.UP, Direction.DOWN, Direction.RIGHT]
        else:
            if deltaX > 0:
                if deltaY > 0:
                    return [Direction.DOWN, Direction.RIGHT, Direction.LEFT, Direction.UP]
                else:
                    return [Direction.UP, Direction.RIGHT, Direction.LEFT, Direction.DOWN]
            else:
                if deltaY > 0:
                    return [Direction.DOWN, Direction.LEFT, Direction.RIGHT, Direction.UP]
                else:
                    return [Direction.UP, Direction.LEFT, Direction.RIGHT, Direction.DOWN]

    def print(self):
        print("---------------------------")
        for y in range(self.height):
            for x in range(self.width):
                if x == self.pos.x and y == self.pos.y:
                    print("X", end=" ")
                else:
                    print(self.tileToString(self.get_tile(x, y)), end=" ")
            print()
        print("---------------------------")

def solve(robot: Robot) -> None:
    robot.print_grid()
    solver = Solver(robot)
    solver.solve()

class Solver:
    def __init__(self, robot: Robot):
        width, height = robot.get_grid_dimensions()
        self.robot = robot
        self.target_pos = robot.get_person_position()
        self.starting_pos = robot.get_exit_position()
        self.map = CustomMap(width, height, self.target_pos, self.starting_pos)
    
    def solve(self):
        self.map.print()
        for i in range(5):
            self.solve_next_step()
            self.map.print()

    def solve_next_step(self):
        self.sense_fire_and_update_map()
        direction = self.map.detect_best_direction()
        self.robot.move(direction)

    def sense_fire_and_update_map(self):
        sense_fire_count = self.robot.sense_fires_around()
        if sense_fire_count == 0:
            self.map.set_tiles_arround([Tile.UNKNOWN], Tile.EMPTY)
            return # No fire around
        
        close_fire_count = map.get_close_count([Tile.FIRE])
        if (close_fire_count == sense_fire_count):
            self.map.set_tiles_arround([Tile.UNKNOWN], Tile.EMPTY)
            return # Fire around, but already identified

        close_empty_or_fire_count = map.get_close_count([Tile.UNKNOWN, Tile.FIRE, Tile.POTENTIAL_FIRE])
        if (sense_fire_count == close_empty_or_fire_count):
            self.map.set_tiles_arround([Tile.UNKNOWN, Tile.POTENTIAL_FIRE], Tile.FIRE)
            return # Number of fire detected is equal to number of unknown squares
        
        self.map.set_tiles_arround([Tile.UNKNOWN], Tile.POTENTIAL_FIRE)
        return # Unknow
