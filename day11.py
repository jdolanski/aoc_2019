from aocd import data
from intcode_machine import run_lazy
import numpy as np


# colors
BLACK = 0
WHITE = 1
# turns
TURN_LEFT = 0
TURN_RIGHT = 1
# facing directons
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3


def run_robot(_intcode, start_color):
    robot = run_lazy(_intcode)
    current_facing = UP
    y = 0
    x = 0
    panels = {}
    for _ in robot:
        current_color = panels.setdefault((y, x), start_color)
        next_color = robot.send(current_color)
        panels[(y, x)] = next_color

        next_turn = next(robot)
        if ((next_turn == TURN_LEFT and current_facing == UP)
                or (next_turn == TURN_RIGHT and current_facing == DOWN)):
            current_facing = LEFT
            x -= 1
        elif ((next_turn == TURN_RIGHT and current_facing == UP)
              or (next_turn == TURN_LEFT and current_facing == DOWN)):
            current_facing = RIGHT
            x += 1
        elif ((next_turn == TURN_LEFT and current_facing == RIGHT)
              or (next_turn == TURN_RIGHT and current_facing == LEFT)):
            current_facing = UP
            y -= 1
        elif ((next_turn == TURN_RIGHT and current_facing == RIGHT)
              or (next_turn == TURN_LEFT and current_facing == LEFT)):
            current_facing = DOWN
            y += 1

    return panels


intcode = data.split(",")

# part A
result = run_robot(intcode, BLACK)
print("Part A", len(result))

# part B
result = run_robot(intcode, WHITE)
dys = list(map(lambda k: k[0], result))
dxs = list(map(lambda k: k[1], result))
grid_h = -min(dys) + max(dys) + 1
grid_w = -min(dxs) + max(dxs) + 1
grid = np.zeros((grid_h, grid_w), dtype=np.int8)

for (y, x), color in result.items():
    grid[y, x] = color

print("Part B")
for row in grid:
    print("".join(map(lambda n: '#' if n == WHITE else '.', row)))
