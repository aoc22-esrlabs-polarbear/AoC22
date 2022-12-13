import re
from pathlib import Path
from typing import Iterable, List, Tuple


def parse_stacks(data: str):
    num_stacks = 9
    stacks = [[] for i in range(num_stacks)]
    lines = data.strip().split('\n')

    for line in lines[:-1]:
        for i in range(num_stacks):
            index = i * 4 + 1
            if index >= len(line):
                continue
            stack = line[index]
            if stack != ' ':
                stacks[i].insert(0, stack)
    return stacks


def parse_moves(data: str, adjust_indices: bool = True) -> List[Tuple[int, int, int]]:
    pattern = r'move (\d+) from (\d+) to (\d+)'
    matches = re.findall(pattern, data, flags=re.MULTILINE)
    moves = [(int(a), int(b), int(c)) for a, b, c in matches]
    if adjust_indices:
        moves = [(int(a), int(b - 1), int(c - 1)) for a, b, c in moves]
    return moves


def read_input():
    data = Path('input05.txt').open('r').read().strip()
    stacks_data, moves_data = data.split('\n\n')
    return parse_stacks(stacks_data), parse_moves(moves_data)


def apply_move_task_1(stacks: List[List[str]], move: Tuple[int, int, int]):
    num, index_from, index_to = move
    carry = [stacks[index_from].pop() for _ in range(num)]
    stacks[index_to].extend(carry)


def apply_move_task_2(stacks: List[List[str]], move: Tuple[int, int, int]):
    num, index_from, index_to = move
    carry = [stacks[index_from].pop() for _ in range(num)]
    stacks[index_to].extend(reversed(carry))


def print_stacks(stacks: List[List[str]]):
    num_rows = max(len(stack) for stack in stacks)
    for row in range(num_rows - 1, -1, -1):
        for i, stack in enumerate(stacks):
            if row < len(stack):
                print(f'[{stack[row]}] ', end='')
            else:
                print('    ', end='')
        print('')

    # print stack numbers
    for i in range(1, len(stacks) + 1):
        print(f' {i}  ', end='')
    print()



def main():
    stacks, moves = read_input()
    print("Stacks at start:")
    print_stacks(stacks)
    for move in moves:
        apply_move_task_1(stacks, move)
    print("Stacks after moves:")
    print_stacks(stacks)
    print("Task 1:", ''.join(stack[-1] for stack in stacks))

    stacks, moves = read_input()
    print("Stacks at start:")
    print_stacks(stacks)
    for move in moves:
        apply_move_task_2(stacks, move)
    print("Stacks after moves:")
    print_stacks(stacks)
    print("Task 2:", ''.join(stack[-1] for stack in stacks))


if __name__ == '__main__':
    main()
