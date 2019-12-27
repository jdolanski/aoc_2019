from aocd import data
from intcode_machine import run_eager

intcode = data.split(",")
# Part A
out = run_eager(intcode, [1])

print("Part A", out)

# Part B
out = run_eager(intcode, [2])

print("Part B", out)
