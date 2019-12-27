from aocd import data
from collections import deque
from multiprocessing.dummy import Pool

WALL = '#'
EMPTY = '.'
ENTRANCE = '@'


def iskey(char):
    return char.isalpha() and char.islower()


def isdoor(char):
    return char.isalpha() and char.isupper()


def find_reachable_keys(maze, start, inventory=frozenset()):
    # list reachable keys from start position considering we have keys in key_bag
    queue = deque([start, None])
    visited = set([start])
    steps = 0
    reachable_keys = {}

    while queue:
        curr_yx = queue.popleft()
        if curr_yx is None:
            steps += 1
            queue.append(None)
            if queue[0] is None:
                break
            else:
                continue

        curr_cell = maze[curr_yx[0]][curr_yx[1]]
        if iskey(curr_cell) and curr_cell not in inventory:
            reachable_keys[curr_cell] = (steps, curr_yx)
        else:
            for r, c in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
                new_yx = (curr_yx[0]+r, curr_yx[1]+c)
                cell = maze[new_yx[0]][new_yx[1]]

                if not(new_yx in visited
                       or cell == WALL
                       or (isdoor(cell) and cell.lower() not in inventory)):
                    visited.add(new_yx)
                    queue.append(new_yx)

    return reachable_keys


def optimal_stepsA(maze, start, inventory=frozenset(), branch_cache={}):
    cache = branch_cache.get((start, inventory))
    if cache:
        return cache

    steps = None
    reachable_keys = find_reachable_keys(maze, start, inventory)
    if not reachable_keys:
        steps = 0
    else:
        for key in reachable_keys:
            key_distance, key_position = reachable_keys[key]
            branch_steps = key_distance + \
                optimal_stepsA(maze, key_position,
                               inventory.union(key), branch_cache)
            if steps is None or branch_steps < steps:
                steps = branch_steps

    branch_cache[(start, inventory)] = steps
    return steps


# part A
maze = data.split('\n')
h = len(maze)
w = len(maze[0])
entrance = None
for y in range(h):
    for x in range(w):
        if maze[y][x] == ENTRANCE:
            entrance = (y, x)

steps = optimal_stepsA(maze, entrance)

print("Part A", steps)

# part B
THREAD_POOL = Pool(4)


def optimal_stepsB(maze, starts, inventory=frozenset(), branch_cache={}):
    def findkeys(robot_pos):
        robot, position = robot_pos
        return robot, find_reachable_keys(maze, position, inventory)

    cache = branch_cache.get((starts, inventory))
    if cache:
        return cache

    robots_keys = THREAD_POOL.map(findkeys, enumerate(starts))
    total_reachable_keys = {}
    for robot, keys in robots_keys:
        for key, (distance, position) in keys.items():
            total_reachable_keys[key] = (robot, distance, position)

    steps = None
    if not total_reachable_keys:
        steps = 0
    else:
        for key, (robot, distance, position) in total_reachable_keys.items():
            new_starts = starts[:robot] + (position,) + starts[robot+1:]
            branch_steps = distance + \
                optimal_stepsB(maze, new_starts,
                               inventory.union(key), branch_cache)
            if steps is None or branch_steps < steps:
                steps = branch_steps

    branch_cache[(starts, inventory)] = steps
    return steps


ey, ex = entrance
updated_maze = maze.copy()
updated_maze[ey-1] = maze[ey-1][:ex-1] + "@#@" + maze[ey-1][ex+2:]
updated_maze[ey+0] = maze[ey+0][:ex-1] + "###" + maze[ey+0][ex+2:]
updated_maze[ey+1] = maze[ey+1][:ex-1] + "@#@" + maze[ey+1][ex+2:]
entrances = ((ey-1, ex-1), (ey-1, ex+1), (ey+1, ex-1), (ey+1, ex+1))


steps = optimal_stepsB(updated_maze, entrances)

print("Part B", steps)
