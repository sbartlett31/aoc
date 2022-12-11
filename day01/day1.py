import heapq
from typing import List

def read_input(fp='./input'):
    res = []
    cur_sum = 0
    with open(fp) as f:
        for x in f:
            if x == '\n':
                res.append(cur_sum)
                cur_sum = 0
            else:
                cur_sum += int(x)
    res.append(cur_sum)
    return res

def get_top_3(in_data: List[int]) -> List[int]:
    heapq.heapify(in_data)
    return heapq.nlargest(3, in_data)

if __name__ == '__main__':
    in_data = read_input()
    print("answer to part 1: ", max(in_data))
    top3 = get_top_3(in_data)
    print(sum(top3))
