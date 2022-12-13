import argparse
import itertools
import pathlib
from typing import Iterable, Tuple, List


TOP, RIGHT, BOTTOM, LEFT = (0, -1), (1, 0), (0, 1), (-1, 0)


def read_input(path: str) -> List[List[int]]:
    content = pathlib.Path(path).open('r').read()
    lines = [line.strip() for line in content.strip().split('\n')]
    return [[int(value) for value in line] for line in lines]


def contains(width: int, height: int, x: int, y: int) -> bool:
    return 0 <= x < width and 0 <= y < height


def walk(grid: List[List[int]], x: int, y: int, direction: Tuple[int, int]) -> Iterable[Tuple[int, int, int]]:
    dx, dy = direction
    x, y = x + dx, y + dy
    while contains(len(grid[0]), len(grid), x, y):
        yield x, y, grid[y][x]
        x, y = x + dx, y + dy


def is_visible(grid: List[List[int]], x: int, y: int) -> bool:
    own_height = grid[y][x]
    for direction in [TOP, RIGHT, BOTTOM, LEFT]:
        if all(height < own_height for _, _, height in walk(grid, x, y, direction)):
            return True
    return False


def scenic_score(grid: List[List[int]], x: int, y: int) -> int:
    score = 1
    own_height = grid[y][x]
    for direction in [TOP, RIGHT, BOTTOM, LEFT]:
        distance = 0
        for _, _, height in walk(grid, x, y, direction):
            distance += 1
            if height >= own_height:
                break
        score *= distance

    return score


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', default='input08.txt')
    args = parser.parse_args()
    grid = read_input(args.input)

    num_visible = 0
    for y, x in itertools.product(range(len(grid)), range(len(grid[0]))):
        num_visible += int(is_visible(grid, x, y))

    print(f'Task 1: {num_visible} trees are visible from the outside.')

    max_scenic_score = 0
    for y, x in itertools.product(range(len(grid)), range(len(grid[0]))):
        max_scenic_score = max(max_scenic_score, scenic_score(grid, x, y))

    print(f'Task 2: max scenic score of {max_scenic_score}.')


if __name__ == '__main__':
    main()
