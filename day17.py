from aocd import data
from intcode_machine_new import IntcodeMachine
import numpy as np

SCAFFOLD = 35
SPACE = 46
NEWLINE = 10

NORTH = 94
SOUTH = 118
EAST = 62
WEST = 60

# turns
LEFT = 76
RIGHT = 82

intcode = data.split(',')

program = IntcodeMachine(intcode)
program.run()

outs = []
row = []
# draw
while True:
    out = program.get_output()
    if out is None:
        break
    elif out == NEWLINE:
        if row:
            print("".join(map(chr, row)))
            outs += [row]
            row = []
        else:
            print('\n')
    else:
        row.append(out)

mat = np.array(outs, dtype=np.int)

intersection = np.array([
    [SPACE, SCAFFOLD, SPACE],
    [SCAFFOLD, SCAFFOLD, SCAFFOLD],
    [SPACE, SCAFFOLD, SPACE]
])

h, w = mat.shape
alignment_param_sum = 0
for r in range(0, h - 3):
    for c in range(0, w - 3):
        if np.array_equal(mat[r:r+3, c:c+3], intersection):
            alignment_param_sum += (r+1)*(c+1)


print("Part A", alignment_param_sum)

# part B


def out_of_bounds(y, x): return y >= h or y < 0 or x >= w or x < 0


rys, rxs = np.where((mat == NORTH) | (mat == SOUTH)
                    | (mat == EAST) | (mat == WEST))
ry, rx = rys[0], rxs[0]

scaffold_insts = []
rr = [-1, 1, 0, 0]
cc = [0, 0, 1, -1]
sides = [NORTH, SOUTH, EAST, WEST]
exclude_idx = set()
facing = mat[ry, rx]
while True:
    side = None
    sideidx = None
    for i in range(4):
        if (not out_of_bounds(ry+rr[i], rx+cc[i])) and (i not in exclude_idx) and (mat[ry+rr[i], rx+cc[i]] == SCAFFOLD):
            sideidx = i
            side = sides[i]
            break
    else:
        break

    if side == NORTH or side == SOUTH:
        exclude_idx = set([0, 1])
    else:
        exclude_idx = set([2, 3])

    if ((side == NORTH and facing == EAST) or (side == SOUTH and facing == WEST)
            or (side == EAST and facing == SOUTH) or (side == WEST and facing == NORTH)):
        scaffold_insts.append(chr(LEFT))
    elif ((side == NORTH and facing == WEST) or (side == SOUTH and facing == EAST)
          or (side == EAST and facing == NORTH) or (side == WEST and facing == SOUTH)):
        scaffold_insts.append(chr(RIGHT))

    facing = side

    count = 0
    while True:
        newy = ry + rr[sideidx]
        newx = rx + cc[sideidx]
        if out_of_bounds(newy, newx) or mat[newy, newx] == SPACE:
            break
        else:
            ry = newy
            rx = newx
            count += 1

    scaffold_insts.append(str(count))

print(",".join(scaffold_insts))

A = list(map(ord, "L,6,L,4,R,12"))
B = list(map(ord, "L,6,R,12,R,12,L,8"))
C = list(map(ord, "L,6,L,10,L,10,L,6"))

SEQUENCE = list(map(ord, "A,B,A,C,B,A,C,B,A,C"))

intcode[0] = '2'
program = IntcodeMachine(intcode)

program.add_inputs(SEQUENCE)
program.add_input(NEWLINE)
program.add_inputs(A)
program.add_input(NEWLINE)
program.add_inputs(B)
program.add_input(NEWLINE)
program.add_inputs(C)
program.add_input(NEWLINE)
program.add_input(ord('n'))
program.add_input(NEWLINE)
program.run()

output = program.get_output()
while True:
    nextout = program.get_output()
    if nextout is None:
        break
    output = nextout

print("Part B", output)
