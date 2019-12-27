from aocd import data
from intcode_machine_new import IntcodeMachine

# strings
intcode = data.split(",")

# part A
machine = IntcodeMachine(intcode, [1])
machine.run()
print("Part A result:", machine.outputs[-1])

# part B
machine = IntcodeMachine(intcode, [5])
machine.run()
print("Part B result:", machine.outputs[-1])
