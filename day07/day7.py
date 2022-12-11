from dataclasses import dataclass, field
from typing import *
from collections import defaultdict
import operator
from pprint import pprint

@dataclass
class DirNode:
    name: str
    size: int=0
    child_dirs: Set['DirNode']=field(default_factory=set)
    child_files: Dict[str, int]=field(default_factory=dict)
    parent: Optional['DirNode']=None

    def __hash__(self):
        if self.parent:
            return hash(f"{self.parent.name}-{self.name}")
        return hash(self.name)

    def mutate_calc_size(self) -> None:
        self.size = sum(self.child_files.values())
        for child in self.child_dirs:
            child.mutate_calc_size()
            self.size += child.size


@dataclass
class Command:
    cmd: str
    args: Optional[str]=None
    output: List[List[str]]=field(default_factory=list)


def parse_input(fp: str='./input') -> List[Command]:
    history = list(map(str.split, open(fp).read().splitlines()))
    i = 0
    res = []
    while i < len(history):
        line = history[i]
        if line[1] == 'cd':
            res.append(Command(cmd='cd', args=line[-1]))
            i += 1
        elif line[1] == 'ls':
            cur_cmd = Command(cmd='ls')
            i += 1
            while i < len(history) and not history[i][0] == '$':
                cur_cmd.output.append(history[i])
                i += 1
            res.append(cur_cmd)
        else:
            raise Exception('parse code is wrong')
    return res


def build_tree(cmds: List[Command]) -> DirNode:
    head = DirNode('/')
    cwd = head
    for cmd in cmds:
        if cmd.cmd == 'cd':
            if cmd.args == '..':
                cwd = cwd.parent
            else:
                cwd = cd_from_parent(cmd.args, cwd)
        if cmd.cmd == 'ls':
            for size, fn in cmd.output:
                if size == 'dir':
                    child = DirNode(fn, parent=cwd)
                    cwd.child_dirs.add(child)
                else:
                    cwd.child_files[fn] = int(size)
    return head

def cd_from_parent(cd_to: str, parent: DirNode) -> DirNode:
    if cd_to == '/' and parent.name == '/':
        return parent
    for child in parent.child_dirs:
        if child.name == cd_to:
            return child


def part1(head: DirNode, upper_threshold=100_000) -> int:
    res = set()

    def traverse(node: DirNode):
        if node.size < upper_threshold:
            res.add(node)
        for child in node.child_dirs:
            traverse(child)
        return

    traverse(head)
    return sum(map(operator.attrgetter('size'), res))

def part2(head: DirNode) -> int:
    max_space = 70000000
    used_space = head.size
    needed_space = 30000000
    need_to_free = needed_space - (max_space - used_space)
    res = set()

    def traverse(node: DirNode):
        if node.size >= need_to_free:
            res.add(node)
        for child in node.child_dirs:
            traverse(child)
        return

    traverse(head)
    return min(res, key=operator.attrgetter('size')).size


if __name__ == '__main__':
    cmds = parse_input()
    root = build_tree(cmds)
    root.mutate_calc_size()
    print(part1(root))
    print(part2(root))
