from aocd import data
import itertools
from intcode_machine import run_eager, run_lazy

intcode = data.split(",")

# part A
results = []
for phases in itertools.permutations([0, 1, 2, 3, 4]):
    outa = run_eager(intcode, [phases[0], 0])[-1]
    outb = run_eager(intcode, [phases[1], outa])[-1]
    outc = run_eager(intcode, [phases[2], outb])[-1]
    outd = run_eager(intcode, [phases[3], outc])[-1]
    oute = run_eager(intcode, [phases[4], outd])[-1]
    results.append(int(oute))

print("Part A", max(results))

# part B
results = []
for phases in itertools.permutations([5, 6, 7, 8, 9]):
    genA = run_lazy(intcode, phases[0])
    genB = run_lazy(intcode, phases[1])
    genC = run_lazy(intcode, phases[2])
    genD = run_lazy(intcode, phases[3])
    genE = run_lazy(intcode, phases[4])

    outE = 0
    for generators in itertools.zip_longest(genA, genB, genC, genD, genE):
        outA = genA.send(outE)
        outB = genB.send(outA)
        outC = genC.send(outB)
        outD = genD.send(outC)
        outE = genE.send(outD)

    results.append(int(outE))

print("Part B", max(results))
