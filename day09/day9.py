from dataclasses import dataclass
from itertools import chain
from typing import *


@dataclass
class Point:
    x: int = 0
    y: int = 0

    def __add__(self, delta: "Delta") -> "Point":
        return Point(self.x + delta.x, self.y + delta.y)

    def __hash__(self):
        return hash((self.x, self.y))


@dataclass
class Delta:
    x: int = 0
    y: int = 0


@dataclass
class Rope:
    knots: List[Point]

    @property
    def head(self):
        return self.knots[0]

    @property
    def tail(self):
        return self.knots[-1]


def clip(val: int, lb=-1, ub=1) -> int:
    return max(lb, min(val, ub))


def calc_distance(p1: Point, p2: Point) -> Delta:
    return Delta(p1.x - p2.x, p1.y - p2.y)


def get_move(head: Point, tail: Point) -> Delta:
    delta = calc_distance(head, tail)
    if abs(delta.x) > 1 or abs(delta.y) > 1:
        return Delta(clip(delta.x), clip(delta.y))
    return Delta(0, 0)


def direction_to_delta(direction: str) -> Delta:
    return {"L": Delta(-1, 0), "R": Delta(1, 0), "U": Delta(0, 1), "D": Delta(0, -1)}[
        direction
    ]


def move_head(rope: Rope, move: Delta) -> Rope:
    new_head = rope.head + move
    res = [new_head]
    for knot in rope.knots[1:]:
        knot_move = get_move(res[-1], knot)
        res.append(knot + knot_move)
    return Rope(res)


def run_sim(moves: str, n_knots: int = 2):
    rope = Rope([Point() for _ in range(n_knots)])
    seen = {rope.tail}
    for direction in moves:
        head_move = direction_to_delta(direction)
        rope = move_head(rope, head_move)
        seen.add(rope.tail)
    return len(seen)


def parse_input(fp="./input"):
    with open(fp) as f:
        lines = map(str.split, f.read().splitlines())
    res = []
    for direction, n_moves in lines:
        res.append(direction * int(n_moves))
    return "".join(chain.from_iterable(res))


if __name__ == "__main__":
    moves = parse_input()
    print(run_sim(moves))
    print(run_sim(moves, 10))
