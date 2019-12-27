from aocd import data
from intcode_machine import run_eager, run_lazy
import numpy as np

EMPTY = 0
WALL = 1
BLOCK = 2
PADDLE = 3
BALL = 4

intcode = data.split(",")

# part A
outs = run_eager(intcode)
blocks = 0

for i in range(2, len(outs), 3):
    if outs[i] == BLOCK:
        blocks += 1

print("Part A", blocks)

# part B
intcode[0] = '2'
game = run_lazy(intcode)
ball_x = None
paddle_x = None
current_score = None

for val in game:
    x = val
    if x is None:
        joy_input = np.clip(ball_x - paddle_x, -1, 1)
        x = game.send(joy_input)

    y = next(game)
    tile = next(game)
    if x == -1 and y == 0:
        current_score = tile
    else:
        if tile == PADDLE:
            paddle_x = x
        elif tile == BALL:
            ball_x = x

print("Part B", current_score)
