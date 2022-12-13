from pathlib import Path
from typing import Iterable


def read_input():
    data = Path('input05.txt').open('r').read().strip()
    stacks_data, moves_data = data.split('\n\n')
    return read_stacks(stacks_data), read_moves(m)



def round_result(opponent: int, us: int) -> int:
    return (us - opponent + 1) % 3


def round_score(opponent: int, us: int) -> int:
    return us + round_result(opponent, us) * 3


def total_score(opponent: Iterable[int], us: Iterable[int]) -> int:
    return sum(round_score(a, b) for a, b in zip(opponent, us))


def find_move_for_result(opponent: int, desired_result: int) -> int:
    # brute force
    for move in [ROCK, PAPER, SCISSORS]:
        if round_result(opponent, move) == desired_result:
            return move
    raise Exception(f'Failed to determine move against {opponent} that results in {desired_result}.')


def main():
    rows = read_input()
    column0, column1 = zip(*rows)

    mapping_abc = {'A': ROCK, 'B': PAPER, 'C': SCISSORS}
    moves_opponent = [mapping_abc[key] for key in column0]

    mapping_xyz = {'X': ROCK, 'Y': PAPER, 'Z': SCISSORS}
    moves_us = [mapping_xyz[key] for key in column1]
    print('(task 1) total predicted score:', total_score(moves_opponent, moves_us))

    mapping_xyz = {'X': LOSE, 'Y': DRAW, 'Z': WIN}
    moves_us = [find_move_for_result(opponent, mapping_xyz[key]) for opponent, key in zip(moves_opponent, column1)]
    print('(task 2) total predicted score:', total_score(moves_opponent, moves_us))


if __name__ == '__main__':
    main()
