from typing import *
import numpy as np
import typer
import sys

sys.setrecursionlimit(3000)


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


def main(fp: str = "./test"):
    xs, ys, zs = read_inputs(fp)
    matrix = make_matrix(xs, ys, zs)
    print(search(matrix))


if __name__ == "__main__":
    typer.run(main)
