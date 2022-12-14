import argparse
from dataclasses import dataclass
from math import log10
from typing import List, Tuple, Iterable, Optional, Callable

ROCK, AIR, SAND = "#.o"
SAND_ORDER = [(0, 1), (-1, 1), (1, 1)]

@dataclass
class Wall:
    x_min: int
    x_max: int
    grid: List[List[str]]

    @property
    def y_max(self) -> int:
        return len(self.grid)

    def get(self, x: int, y: int) -> str:
        return self.grid[y][x - self.x_min]

    def set(self, x: int, y: int, value: str):
        self.grid[y][x - self.x_min] = value

    def count(self, value: str) -> int:
        return sum(sum([1 for v in row if v == value]) for row in self.grid)


def sign(value: int) -> int:
    if value > 0:
        return 1
    elif value < 0:
        return -1
    return 0


def signed_range(a: int, b: int) -> range:
    return range(a, b, sign(b - a))


def iterate_path(path: List[Tuple[int, int]]) -> Iterable[Tuple[int, int]]:
    if len(path) == 0:
        return

    for i in range(1, len(path)):
        start, end = path[i - 1], path[i]
        if start[0] != end[0]:
            for x in range(start[0], end[0], sign(end[0] - start[0])):
                yield x, start[1]
        elif start[1] != end[1]:
            for y in range(start[1], end[1], sign(end[1] - start[1])):
                yield start[0], y
    yield path[-1]


def create_wall(paths: List[List[Tuple[int, int]]], with_bottom: bool) -> Wall:
    x_min = min((min(x for x, _ in path)) for path in paths)
    x_max = max((max(x for x, _ in path)) for path in paths)
    y_max = max((max(y for _, y in path)) for path in paths)

    x_space = 2
    if with_bottom:
        y_max += 2
        x_space = y_max * 2  # close enough to infinite

    x_min, x_max = x_min - x_space, x_max + x_space  # extend left and right by 2 so sand can fall freely
    num_columns = x_max - x_min + 1
    grid = [[AIR, ] * num_columns for _ in range(y_max + 1)]
    wall = Wall(x_min, x_max, grid)

    for path in paths:
        for i, (x, y) in enumerate(iterate_path(path)):
            wall.set(x, y, ROCK)

    if with_bottom:
        wall.grid[-1] = ROCK * len(wall.grid[-1])

    return wall


def propagate_sand(wall: Wall, sand: Tuple[int, int]) -> Optional[Tuple[int, int]]:
    def propagate_once(coordinate: Tuple[int, int]) -> Tuple[bool, Optional[Tuple[int, int]]]:
        x, y = coordinate
        for dx, dy in SAND_ORDER:
            if (y + dy) >= len(wall.grid):
                return True, None

            if wall.get(x + dx, y + dy) == AIR:
                return True, (x + dx, y + dy)

        return False, coordinate

    can_propagate = True
    while can_propagate and sand is not None:
        can_propagate, sand = propagate_once(sand)
    return sand


def fill_sand(wall: Wall, sand_source: Tuple[int, int], n_max: int = 1000,
              stop_condition: Optional[Callable[[Wall], bool]] = None) -> int:
    for i in range(n_max):
        if callable(stop_condition) and stop_condition(wall):
            break
        final_position = propagate_sand(wall, sand_source)
        if final_position is None:
            return i
        wall.set(*final_position, SAND)
    return n_max


def print_wall(wall: Wall, tick_step: int = 2):
    max_column_digits = int(log10(wall.x_max)) + 1
    max_row_digits = int(log10(wall.y_max)) + 1

    for y in range(max_column_digits - 1, -1, -1):
        print(' ' * (max_row_digits + 1), end='')
        for x in range(wall.x_min, wall.x_max + 1, tick_step):
            print(f'{x}'[y], end=' ' * (tick_step - 1))
        print()

    for y in range(wall.y_max):
        y_str = ' ' * (max_row_digits  - len(f'{y}')) + f'{y} '
        print(y_str + ''.join(wall.grid[y]))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', default='input14.txt')
    args = parser.parse_args()

    content = open(args.input, 'r').read().strip()
    lines = [line.strip() for line in content.split('\n')]
    paths = [[tuple(map(int, coordinate.split(','))) for coordinate in line.split(' -> ')] for line in lines]

    wall = create_wall(paths, with_bottom=False)
    sand_source = (500, 0)
    fill_sand(wall, sand_source, 10000)
    print(f'Task 1: {wall.count(SAND)} sand units have come to rest.')

    wall = create_wall(paths, with_bottom=True)

    def stop_condition(_wall: Wall) -> bool:
        return _wall.get(*sand_source) == SAND

    fill_sand(wall, sand_source, 100000, stop_condition)
    print(f'Task 2: {wall.count(SAND)} sand units have come to rest.')



if __name__ == '__main__':
    main()
