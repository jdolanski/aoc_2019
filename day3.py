import numpy as np
from aocd import data

O = 0
EMPTY = 1
W1 = 2
W2 = 3
ISECTION = 4


def pretty_print_2dgrid(grid):
    dic = {
        O: 'O',
        EMPTY: '-',
        W1: 'I',
        W2: 'L',
        ISECTION: 'X'
    }
    out_put = [" ".join([dic[val] for val in row]) for row in grid]
    for row in out_put:
        print(row)


def process_steps(wire):
    x_O_distance = 0
    y_O_distance = 0
    wire_x_steps = []
    wire_y_steps = []
    for step in wire:
        direction = step[0]
        amount = int(step[1:])
        if direction == 'L':
            x_O_distance -= amount
        elif direction == 'R':
            x_O_distance += amount
        elif direction == 'U':
            y_O_distance -= amount
        elif direction == 'D':
            y_O_distance += amount
        wire_y_steps.append(y_O_distance)
        wire_x_steps.append(x_O_distance)

    return wire_y_steps, wire_x_steps


def get_vec_idxs(prev_row, prev_col, row, col):
    if prev_col < col:
        return row, row+1, prev_col+1, col+1
    elif prev_col > col:
        return row, row+1, col, prev_col
    elif prev_row < row:
        return prev_row+1, row+1, col, col+1
    elif prev_row > row:
        return row, prev_row, col, col+1


def draw_wires(grid, O_coords, w1_ys, w1_xs, w2_ys, w2_xs):
    def wire1_fun(vec):
        vec[:] = W1

    def wire2_fun(vec):
        vec[np.where(vec == EMPTY)] = W2
        vec[np.where(vec == W1)] = ISECTION

    def draw_wire(grid, offset_ys, offset_xs, apply_fun):
        prev_row = O_coords[0]
        prev_col = O_coords[1]

        for y, x in zip(offset_ys, offset_xs):
            row = O_coords[0] + y
            col = O_coords[1] + x

            fr, tr, fc, tc = get_vec_idxs(prev_row, prev_col, row, col)
            apply_fun(grid[fr:tr, fc:tc])

            prev_row = row
            prev_col = col

    draw_wire(grid, w1_ys, w1_xs, wire1_fun)
    draw_wire(grid, w2_ys, w2_xs, wire2_fun)


def record_wire_steps_to_isections(grid, O_coords, w_ys, w_xs):
    steps = 0
    isections_records = {}
    prev_row = O_coords[0]
    prev_col = O_coords[1]

    for y, x in zip(w_ys, w_xs):
        row = O_coords[0] + y
        col = O_coords[1] + x

        fr, tr, fc, tc = get_vec_idxs(prev_row, prev_col, row, col)
        vec = grid[fr:tr, fc:tc]
        sliced_idxs = np.where(vec == ISECTION)

        for i_y, i_x in zip(sliced_idxs[0]+fr, sliced_idxs[1]+fc):
            if not isections_records.get((i_y, i_x)):
                # Can use Manhattan distance
                isections_records[(i_y, i_x)] = steps + \
                    abs(prev_row - i_y) + abs(prev_col - i_x)

        steps += max(vec.shape)

        prev_row = row
        prev_col = col

    return isections_records


[w1, w2] = data.split("\n")
w1 = w1.split(",")
w2 = w2.split(",")

# distances of grid edges from O
w1_ys, w1_xs = process_steps(w1)
w2_ys, w2_xs = process_steps(w2)
yx_range = (min(w1_ys + w2_ys), max(w1_ys + w2_ys),
            min(w1_xs + w2_xs), max(w1_xs + w2_xs))

grid_h = -yx_range[0] + yx_range[1] + 1
grid_w = -yx_range[2] + yx_range[3] + 1

grid = np.ones((grid_h, grid_w), dtype=np.int8)

# 0 = O, 1 = empty space, 2 = wire1 steps, 3 = wire2 steps, 4 = intersection
# place O (y, x)
O_coords = (-yx_range[0], -yx_range[2])
grid[O_coords[0], O_coords[1]] = O
# draw wire 1 and intersections of w1 and w2 on grid
draw_wires(grid, O_coords, w1_ys, w1_xs, w2_ys, w2_xs)
# intersection coordinates
iy, ix = np.where(grid == ISECTION)
# get closest intersection to O by Manhattan distance
dy = abs(O_coords[0] - iy[0])
dx = abs(O_coords[1] - ix[0])
min_distance = dy + dx
for y, x in zip(iy[1:], ix[1:]):
    dy = abs(O_coords[0] - y)
    dx = abs(O_coords[1] - x)
    distance = dy + dx
    if distance < min_distance:
        min_distance = distance

print("Min Manhattan distance", min_distance)

# Part B
w1_step_records = record_wire_steps_to_isections(grid, O_coords, w1_ys, w1_xs)
w2_step_records = record_wire_steps_to_isections(grid, O_coords, w2_ys, w2_xs)
steps = []
for yx in w1_step_records.keys():
    steps.append(w1_step_records[yx] + w2_step_records[yx])

print("Min steps", min(steps))
