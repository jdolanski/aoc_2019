from aocd import data
from collections import deque
from intcode_machine_new import IntcodeMachine


def flush_out(program):
    while True:
        out = program.get_output()
        if out is None:
            break


# part A
intcode = data.split(',')
# (~A + ~B + ~C) and D
instructions = """
NOT A J
NOT B T
OR T J
NOT C T
OR T J
AND D J
WALK
""".lstrip('\n')
int_instructions = list(map(ord, instructions))

program = IntcodeMachine(intcode)
program.run()
flush_out(program)
program.add_inputs(int_instructions)
program.run()

outs = []
success_out = None
while True:
    out = program.get_output()
    if out is None:
        break
    if out < 128:
        outs.append(chr(out))
    else:
        success_out = out
last_moments = "".join(outs)
print(last_moments)

print("Part A", success_out)

# part B
# if jump from part A is satisfied, check if E(D+1) or H(D+4) are also true
# if jump from part A is not satisfied, E and H is ignored
instructions = """
OR A T
AND B T
AND C T
NOT T J
AND D J
NOT J T
OR E T
OR H T
AND T J
RUN
""".lstrip('\n')
int_instructions = list(map(ord, instructions))

program = IntcodeMachine(intcode)
program.run()
flush_out(program)
program.add_inputs(int_instructions)
program.run()

outs = []
success_out = None
while True:
    out = program.get_output()
    if out is None:
        break
    if out < 128:
        outs.append(chr(out))
    else:
        success_out = out
last_moments = "".join(outs)

print(last_moments)

print("Part B", success_out)
