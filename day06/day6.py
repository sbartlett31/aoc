from collections import defaultdict

buffer = open('./input').read().strip()

def sliding_window(buffer: str, window_size=4) -> int:
    l = 0
    r = 0
    window = defaultdict(int)
    while r < window_size:
        window[buffer[r]] += 1
        r += 1

    while max(window.values()) > 1 and r < len(buffer):
        window[buffer[l]] -= 1
        l += 1

        window[buffer[r]] += 1
        r += 1
    return r


if __name__ == '__main__':
    part1_res = sliding_window(buffer)
    print(part1_res)
    part2_res = sliding_window(buffer, window_size=14)
    print(part2_res)
