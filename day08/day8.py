import numpy as np
import cytoolz as toolz
from nptyping import NDArray, Int, Shape
from typing import *
from dataclasses import dataclass
from functools import reduce
import operator


def read_input(fp="./input") -> NDArray[Shape["*, *"], Int]:
    with open(fp) as f:
        return toolz.pipe(
            f.read(),
            str.splitlines,
            toolz.curried.map(list),
            list,
            np.asarray,
            lambda arr: arr.astype(np.int8),
        )


def get_viz_array(arr: NDArray[Shape["*, 1"], Int]) -> NDArray[Shape["*, 1"], Int]:
    cur_max = float("-inf")
    res = np.zeros_like(arr)
    for i, x in enumerate(arr):
        if x > cur_max:
            res[i] = 1
            cur_max = x
    return res


def get_viz_matrix(arr: NDArray[Shape["*, *"], Int]) -> NDArray[Shape["*, *"], Int]:
    rows, cols = arr.shape
    from_left = np.asarray([get_viz_array(row) for row in arr])
    from_right = np.asarray([get_viz_array(row[::-1])[::-1] for row in arr])
    from_top = np.asarray([get_viz_array(arr[:, i]) for i in range(cols)]).T
    from_bottom = np.asarray(
        [get_viz_array(arr[:, i][::-1])[::-1] for i in range(cols)]
    ).T
    full_viz = from_left + from_right + from_top + from_bottom
    return np.clip(full_viz, a_min=0, a_max=1)


def get_viz_score_from_element(arr, i, j) -> int:
    to_top = toolz.pipe(get_view_to_top_array(arr, i, j), get_viz_array_part2(arr[i, j]), np.sum)
    to_left = toolz.pipe(get_view_to_left_array(arr, i, j), get_viz_array_part2(arr[i, j]), np.sum)
    to_bottom = toolz.pipe(get_view_to_bottom_array(arr, i, j), get_viz_array_part2(arr[i, j]), np.sum)
    to_right = toolz.pipe(get_view_to_right_array(arr, i, j), get_viz_array_part2(arr[i, j]), np.sum)
    return reduce(operator.mul, [to_top, to_bottom, to_left, to_right])

def get_view_to_top_array(arr, i, j) -> NDArray:
    return arr[:i, j][::-1]

def get_view_to_bottom_array(arr, i, j) -> NDArray:
    return arr[i + 1:, j]

def get_view_to_left_array(arr, i, j) -> NDArray:
    return arr[i, :j][::-1]

def get_view_to_right_array(arr, i, j) -> NDArray:
    return arr[i, j + 1:]

@toolz.curry
def get_viz_array_part2(threshold: int, arr: NDArray[Shape["*, 1"], Int]) -> NDArray[Shape["*, 1"], Int]:
    res = np.zeros_like(arr)
    for i, x in enumerate(arr):
        res[i] = 1
        if x >= threshold:
            return res
    return res



def part2_lol(arr) -> int:
    res = []
    for i, row in enumerate(arr):
        for j, ele in enumerate(row):
            res.append(get_viz_score_from_element(arr, i, j))
    return max(res)


if __name__ == "__main__":
    data = read_input()
    viz_matrix = get_viz_matrix(data)
    print(viz_matrix.sum())
    print(part2_lol(data))

@dataclass
class DPElement:
    n_viz: int
    max_height: int
    max_height_loc: int
    this_height: int


def part2_dp(arr: NDArray) -> NDArray:
    """
    plan is to create 4 DP arrays (1 from each direction) where each element is a DPElement
    recurrence =
        if prev element (i.e., one preceding current element in relevant direction) this_height < max_height
            if prev element.this_height >= prev prev element.this_height:
                return n_viz
            if prev_element.this_height < prev prev element.this_height:
                return 1
    """
    res = np.zeros_like(arr)


