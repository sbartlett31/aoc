from typing import *

SCORE_MAP = {
 "X": 1,
 "Y": 2,
 "Z": 3,
}

WIN_PTS = 6
DRAW_PTS = 3
LOSE_PTS = 0

WIN_MAP = dict(zip('ABC', 'YZX'))
DRAW_MAP = dict(zip('ABC', 'XYZ'))
LOSE_MAP = dict(zip('ABC', 'ZXY'))

def read_input(fp: str='./input') -> List[Tuple[str]]:
    return list(map(str.split, open(fp).readlines()))

def score_round(first: str, second: str, score_map=SCORE_MAP, get_second_play: Callable[[str, str], str]=lambda x, y: y) -> int:
    second_play = get_second_play(first, second)
    base_score = SCORE_MAP[second_play]
    for play_map, pts in zip([WIN_MAP, DRAW_MAP, LOSE_MAP], [WIN_PTS, DRAW_PTS, LOSE_PTS]):
        if second_play == play_map[first]:
            return base_score + pts

def get_second_play_part_2(elf: str, outcome: str) -> str:
    if outcome == 'Y':
        return DRAW_MAP[elf]
    if outcome == 'X':
        return LOSE_MAP[elf]
    return WIN_MAP[elf]

if __name__ == '__main__':
    games = read_input()
    part1_answer = sum(map(lambda x: score_round(*x), games))
    print('part1:', part1_answer)
    part2_answer = sum(map(lambda x: score_round(*x, get_second_play=get_second_play_part_2), games))
    print('part2:', part2_answer)
