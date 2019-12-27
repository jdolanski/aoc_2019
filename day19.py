from aocd import data
from intcode_machine_new import IntcodeMachine
import numpy as np


intcode = data.split(',')

# part A
h, w = 50, 50
area_map = np.empty((h, w), dtype=np.int8)

program = IntcodeMachine(intcode)

for y in range(h):
    for x in range(w):
        program.add_inputs([x, y])
        program.run()
        area_map[y, x] = program.get_output()
        program.reset()

print("Part A", np.count_nonzero(area_map))

# part B
program = IntcodeMachine(intcode)

# bruteforce it
x = 0
y = 0
answer = None
while True:
    program.reset()
    program.add_inputs([x, y])
    program.run()
    out = program.get_output()
    if out == 0:
        y += 1
    else:
        program.reset()
        program.add_inputs([x, y + 99])
        program.run()
        out = program.get_output()
        if out == 0:
            x += 100
        else:
            program.reset()
            program.add_inputs([x - 99, y + 99])
            program.run()
            out = program.get_output()
            if out == 0:
                x += 1
            else:
                answer = (x - 99)*10000 + y
                break

print("Part B", answer)
