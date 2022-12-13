import argparse
from pathlib import Path
from typing import Tuple, Iterable


def arg_max(values: Iterable[int]) -> Tuple[int, int]:
    max_index, max_value = -1, 0
    for index, value in enumerate(values):
        if value > max_value:
            max_index, max_value = index, value
    return max_index, max_value


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    args = parser.parse_args()
    input_str = Path(args.input).open('r').read()
    calories_per_elf = [[int(calories_str) for calories_str in chunk.split('\n')] for chunk in input_str.split('\n\n')]
    calories_sum_per_elf = [sum(calories) for calories in calories_per_elf]
    max_index, max_value = arg_max(calories_sum_per_elf)
    print('1', max_index, max_value)

    calories_sum_per_elf = sorted(calories_sum_per_elf, reverse=True)
    print('2', sum(calories_sum_per_elf[:3]))


if __name__ == '__main__':
    main()
