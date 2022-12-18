from typing import *
import numpy as np
import typer
import sys
import copy

sys.setrecursionlimit(10_000)


def read_inputs(fp: str = "./test") -> Tuple[List[int], List[int], List[int]]:
    xs = []
    ys = []
    zs = []
    with open(fp) as f:
        indices = f.read().splitlines()
    for line in indices:
        x, y, z = map(int, line.split(","))
        xs.append(x)
        ys.append(y)
        zs.append(z)
    return xs, ys, zs


def make_matrix(xs, ys, zs) -> np.ndarray:
    matrix = np.zeros(shape=(max(xs) + 2, max(ys) + 2, max(zs) + 2))
    for x, y, z in zip(xs, ys, zs):
        matrix[x, y, z] = 1
    return matrix


def search(matrix: np.ndarray) -> int:
    n_sides = []
    visited = set()

    def dfs(x, y, z):
        if (x, y, z) in visited:
            return
        visited.add((x, y, z))
        sides_visible = 0
        for offset in [-1, 1]:
            if matrix[x + offset, y, z] == 0:
                sides_visible += 1
            else:
                dfs(x + offset, y, z)

            if matrix[x, y + offset, z] == 0:
                sides_visible += 1
            else:
                dfs(x, y + offset, z)

            if matrix[x, y, z + offset] == 0:
                sides_visible += 1
            else:
                dfs(x, y, z + offset)
        n_sides.append(sides_visible)
        return

    for x, y, z in np.ndindex(*matrix.shape):
        if matrix[x, y, z] == 1 and (x, y, z) not in visited:
            dfs(x, y, z)

    return sum(n_sides)


def get_unreachable(matrix: np.ndarray) -> Set[Tuple[int, int, int]]:
    copied = copy.deepcopy(matrix)

    def dfs(x, y, z):
        copied[x, y, z] = 1
        for offset in [-1, 1]:
            if 0 <= (x + offset) < copied.shape[0] and copied[x + offset, y, z] == 0:
                dfs(x + offset, y, z)

            if 0 <= (y + offset) < copied.shape[1] and copied[x, y + offset, z] == 0:
                dfs(x, y + offset, z)

            if 0 <= (z + offset) < copied.shape[2] and copied[x, y, z + offset] == 0:
                dfs(x, y, z + offset)
        return

    dfs(0, 0, 0)
    res = set()

    for x, y, z in np.ndindex(*matrix.shape):
        if copied[x, y, z] == 0:
            res.add((x, y, z))

    return res


def main(fp: str = "./test"):
    xs, ys, zs = read_inputs(fp)
    matrix = make_matrix(xs, ys, zs)
    print(search(matrix))

    ignore_nodes = get_unreachable(matrix)
    for x, y, z in ignore_nodes:
        matrix[x, y, z] = 1

    print(search(matrix))


if __name__ == "__main__":
    typer.run(main)
