from __future__ import annotations
from itertools import cycle
from typing import *
from dataclasses import dataclass, field
from classes import *
import typer
from collections import deque

wind_map: Dict[str, Delta] = {"<": Delta(x=-1), ">": Delta(x=1)}


def get_jetstream(fp: str = "./test") -> str:
    with open(fp) as f:
        return cycle(f.read().strip())


def wind_to_delta(wind: str) -> Delta:
    return wind_map[wind]


@dataclass
class TetrisGame:
    wind_gen: Iterable[str]
    width: int = 6
    piece_gen = cycle([MinusPiece, PlusPiece, LPiece, LongPiece, SquarePiece])
    placed: Deque[Piece] = field(default_factory=deque)

    def place_rock(self) -> TetrisGame:
        rock = next(self.piece_gen).spawn(self.max_height + 3)
        wind: str = next(self.wind_gen)
        while True:
            rock = self.move(rock, wind)
            fallen_rock = self.fall(rock)
            if rock == fallen_rock:
                self.placed.appendleft(rock)
                return self
            rock = fallen_rock
            wind: str = next(self.wind_gen)

    def move(self, rock: Piece, wind: str) -> Piece:
        if wind == "<" and rock.min_left == 0:
            return rock
        if wind == ">" and rock.max_right == self.width:
            return rock

        wind_delta = wind_to_delta(wind)
        next_piece = rock + wind_delta
        if any(plcd.intersect(next_piece) for plcd in self.placed):
            return rock
        return next_piece

    def fall(self, rock: Piece) -> Piece:
        if rock.bottom_point == 0:
            return rock
        next_piece = rock + Delta(y=-1)
        if any(plcd.intersect(next_piece) for plcd in self.placed):
            return rock
        return next_piece

    def play(self, n_rounds: int) -> TetrisGame:
        for i in range(n_rounds):
            if not i % 25:
                print(i)
            self.place_rock()
        return self

    @property
    def max_height(self) -> int:
        return max(p.max_height for p in self.placed) + 1 if self.placed else 0


def main(fp: str = "./test", n_rounds: int = 2022):
    wind = get_jetstream(fp)
    tetris = TetrisGame(wind_gen=wind)
    tetris.play(n_rounds)
    print(tetris.max_height)


if __name__ == "__main__":
    typer.run(main)
