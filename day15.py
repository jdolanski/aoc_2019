from aocd import data
from intcode_machine_new import IntcodeMachine
from collections import deque


NORTH = 1
SOUTH = 2
WEST = 3
EAST = 4

WALL = 0
EMPTY = 1
OXYGEN = 2

intcode = data.split(',')

# part A


def bfs(initial_robot: IntcodeMachine):
    queue = deque([(initial_robot, (0, 0)), None])
    discovered = {(0, 0): EMPTY}
    steps = 0

    while queue:
        temp = queue.popleft()
        if temp is None:
            steps += 1
            queue.append(None)
            if queue[0] is None:
                break
            else:
                continue

        robot, curr_yx = temp
        if discovered[curr_yx] == OXYGEN:
            return steps
        else:
            nsew = [(NORTH, (-1, 0)), (SOUTH, (1, 0)),
                    (EAST, (0, 1)), (WEST, (0, -1))]
            for side in nsew:
                new_y = curr_yx[0] + side[1][0]
                new_x = curr_yx[1] + side[1][1]
                new_yx = (new_y, new_x)
                if new_yx not in discovered:
                    # start the robot from current robot state
                    new_robot = robot.clone_state()
                    new_robot.add_input(side[0])
                    new_robot.run()
                    status = new_robot.get_output()
                    discovered[new_yx] = status
                    if status != WALL:
                        queue.append((new_robot, new_yx))

    return steps


steps = bfs(IntcodeMachine(intcode))

print("Part A", steps)

# part B


def bfs_explore_map(initial_robot: IntcodeMachine):
    queue = deque([(initial_robot, (0, 0))])
    discovered = {(0, 0): EMPTY}
    oxygen_location = None

    while queue:
        robot, curr_yx = queue.popleft()

        if discovered[curr_yx] == OXYGEN:
            oxygen_location = curr_yx

        nsew = [(NORTH, (-1, 0)), (SOUTH, (1, 0)),
                (EAST, (0, 1)), (WEST, (0, -1))]
        for side in nsew:
            new_y = curr_yx[0] + side[1][0]
            new_x = curr_yx[1] + side[1][1]
            new_yx = (new_y, new_x)
            if new_yx not in discovered:
                # start the robot from current robot state
                new_robot = robot.clone_state()
                new_robot.add_input(side[0])
                new_robot.run()
                status = new_robot.get_output()
                discovered[new_yx] = status
                if status != WALL:
                    queue.append((new_robot, new_yx))

    return discovered, oxygen_location


def bfs_oxygen_spread(area_map: dict, oxygen_yx):
    queue = deque([oxygen_yx, None])
    visited = set(oxygen_yx)
    # the first minute does not count
    minutes = -1

    while queue:
        curr_yx = queue.popleft()
        if curr_yx is None:
            minutes += 1
            queue.append(None)
            if queue[0] is None:
                break
            else:
                continue

        nsew = [(-1, 0), (1, 0), (0, 1), (0, -1)]
        for side in nsew:
            new_yx = (curr_yx[0] + side[0], curr_yx[1] + side[1])
            if new_yx not in visited:
                visited.add(new_yx)
                if area_map[new_yx] != WALL:
                    queue.append(new_yx)

    return minutes


area_map, oxygen_yx = bfs_explore_map(IntcodeMachine(intcode))
minutes = bfs_oxygen_spread(area_map, oxygen_yx)
print("Part B", minutes)
