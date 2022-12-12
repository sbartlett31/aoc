import heapq
import string
import cytoolz as toolz
import typer
from typing import *

Grid = List[List[str]]
Path = Tuple[int, List[Tuple[int, int]]]


def read_input(fp: str = "./input") -> Grid:
    with open(fp) as f:
        return toolz.pipe(
            f.read(),
            str.splitlines,
            toolz.curried.map(list),
            list,
        )


def bfs(data: Grid, start_values=["S"]):
    starts = get_locations(data, start_values)
    end_loc = get_locations(data, "E")[0]
    q: List[Path] = [(1, [start_loc]) for start_loc in starts]
    seen: Set[Tuple[int, int]] = set(starts)
    while q:
        cur_len, cur_path = heapq.heappop(q)
        cur_loc = cur_path[-1]
        for nb in get_neighbors(data, cur_loc):
            if nb == end_loc:
                return cur_len + 1
            elif nb not in seen:
                seen.add(nb)
                heapq.heappush(q, (cur_len + 1, cur_path + [nb]))
    raise ValueError("No path found")


def get_locations(data: Grid, point_vals=["S"]) -> List[Tuple[int, int]]:
    res = []
    for i, row in enumerate(data):
        for j, element in enumerate(row):
            if element in point_vals:
                res.append((i, j))
    return res


def get_neighbors(grid: Grid, cur_loc: Tuple[int, int]) -> Iterable[Tuple[int, int]]:
    res = []
    i, j = cur_loc
    cur_value = get_value(grid[i][j])
    max_i = len(grid)
    max_j = len(grid[0])
    for offset in [-1, 1]:
        next_i = i + offset
        next_j = j + offset
        if 0 <= next_i < max_i and get_value(grid[next_i][j]) <= (cur_value + 1):
            res.append((next_i, j))
        if 0 <= next_j < max_j and get_value(grid[i][next_j]) <= (cur_value + 1):
            res.append((i, next_j))
    return res


def get_value(element: str) -> int:
    if element == "S":
        return 0
    if element == "E":
        return 25
    return string.ascii_lowercase.index(element)


def main(fp: str):
    data = read_input(fp)
    print(bfs(data) - 1)
    print(bfs(data, start_values=["S", "a"]) - 1)


if __name__ == "__main__":
    typer.run(main)
