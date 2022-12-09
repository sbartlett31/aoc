from typing import *

def main() -> None:
    data = read_input()
    print(sum(full_overlap(*assignment) for assignment in data))
    print(sum(partial_overlap(*assignment) for assignment in data))

def read_input(fp: str="./input") -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
    def split_line(line: str) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        pairs = line.split(',')
        pair1, pair2 = pairs[0].split('-'), pairs[1].split('-')
        return tuple(map(int, pair1)), tuple(map(int, pair2))

    return [split_line(l) for l in open(fp).read().splitlines()]

def full_overlap(pair1: Tuple[int, int], pair2: Tuple[int, int]) -> bool:
    return (
    pair1[0] >= pair2[0] and pair1[1] <= pair2[1]
    or
    pair2[0] >= pair1[0] and pair2[1] <= pair1[1]
    )

def partial_overlap(pair1: Tuple[int, int], pair2: Tuple[int, int]) -> bool:
    return (
    pair2[0] <= pair1[0] <= pair2[1]
    or pair2[0] <= pair1[1] <= pair2[1]
    or pair1[0] <= pair2[0] <= pair1[1]
    or pair1[0] <= pair2[1] <= pair1[1]
    )


if __name__ == '__main__':
    main()
