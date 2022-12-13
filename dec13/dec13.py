import argparse
from ast import literal_eval
from functools import cmp_to_key, reduce
from typing import List, Union


def compare_packets(value0: Union[int, List], value1: Union[int, List]) -> int:
    if isinstance(value0, int) and isinstance(value1, int):
        return value0 - value1
    elif isinstance(value0, list) and isinstance(value1, list):
        for item0, item1 in zip(value0, value1):
            compare_result = compare_packets(item0, item1)
            if compare_result != 0:
                return compare_result
        return len(value0) - len(value1)

    value0, value1 = ([value0], value1) if isinstance(value0, int) else (value0, [value1])
    return compare_packets(value0, value1)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', default='input13.txt')
    args = parser.parse_args()

    content = open(args.input, 'r').read().strip()
    pairs = [tuple(literal_eval(line) for line in block.split('\n')) for block in content.split('\n\n')]

    indices_in_order = [i + 1 for i, pair in enumerate(pairs) if compare_packets(*pair) < 0]
    print(f'Task 1: Sum of pair indices in right order: {sum(indices_in_order)}.')

    divider_packets = ([[2]], [[6]])
    packets = list(divider_packets)
    for pair in pairs:
        packets.extend(pair)

    packets_sorted = sorted(packets, key=cmp_to_key(compare_packets))
    divider_packet_indices = [i + 1 for i, packet in enumerate(packets_sorted) if packet in divider_packets]
    print(f'Task 2: Product of divider packet indices: {reduce(lambda a, b: a * b, divider_packet_indices)}.')


if __name__ == '__main__':
    main()
