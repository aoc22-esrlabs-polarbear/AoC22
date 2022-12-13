import argparse
import itertools
import pathlib
import string
from typing import List, Tuple, Iterable


Grid = List[List[int]]
Position = Tuple[int, int]

DIRECTIONS = (UP, RIGHT, DOWN, LEFT) = ((0, -1), (1, 0), (0, 1), (-1, 0))


def read_input(path: str) -> Tuple[Grid, Position, Position]:
    content = pathlib.Path(path).open('r').read().strip()
    lines = [line.strip() for line in content.strip().split('\n')]

    start_position, best_signal = (-1, -1), (-1, -1)
    grid = []

    for y, line in enumerate(lines):
        row = []
        for x, letter in enumerate(line):
            if letter == 'S':
                start_position = (x, y)
                letter = 'a'
            elif letter == 'E':
                best_signal = (x, y)
                letter = 'z'

            row.append(string.ascii_lowercase.index(letter))
        grid.append(row)
    return grid, start_position, best_signal



def get_neighbors(grid: Grid, position: Position) -> Iterable[Position]:
    width, height = len(grid[0]), len(grid)
    for dx, dy in DIRECTIONS:
        x, y = position[0] + dx, position[1] + dy
        if 0 <= x < width and 0 <= y < height:
            yield x, y


def get_possible_neighbors(grid: Grid, position: Position) -> Iterable[Position]:
    current_elevation = grid[position[1]][position[0]]
    for neighbor in get_neighbors(grid, position):
        elevation = grid[neighbor[1]][neighbor[0]]
        if (elevation - current_elevation) <= 1:
            yield neighbor


def find_shortest_way(grid: Grid, start_position: Position, goal_position: Position) -> int:
    max_distance = len(grid) * len(grid[0]) + 1
    start_distance_grid = [[max_distance, ] * len(row) for row in grid]
    start_distance_grid[start_position[1]][start_position[0]] = 0
    queue = [start_position]

    while len(queue) > 0:
        position = queue.pop(0)
        current_distance = start_distance_grid[position[1]][position[0]]

        possible_neighbors = list(get_possible_neighbors(grid, position))
        for neighbor in possible_neighbors:
            if (current_distance + 1) < start_distance_grid[neighbor[1]][neighbor[0]]:
                start_distance_grid[neighbor[1]][neighbor[0]] = current_distance + 1
                queue.append(neighbor)

    shortest_way = start_distance_grid[goal_position[1]][goal_position[0]]
    return shortest_way


def find_shortest_trail(grid: Grid, goal_position: Position) -> int:
    # brute force
    width, height, = len(grid[0]), len(grid)
    starts = filter(lambda start: grid[start[1]][start[0]] == 0, itertools.product(range(width), range(height)))
    return min([find_shortest_way(grid, start, goal_position) for start in starts])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', default='input12.txt')
    args = parser.parse_args()

    grid, start, best_reception = read_input(args.input)
    print(f'Task 1: Shortest way in {find_shortest_way(grid, start, best_reception)} steps.')
    print(f'Task 2: Shortest trail in {find_shortest_trail(grid, best_reception)} steps.')


if __name__ == '__main__':
    main()
