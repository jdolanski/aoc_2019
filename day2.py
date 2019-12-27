from aocd import data


def program(intcode, noun, verb):
    def add(intcode, pos):
        p_lhs, p_rhs, p_dest = intcode[pos + 1], intcode[pos + 2], intcode[pos + 3]
        intcode[p_dest] = intcode[p_lhs] + intcode[p_rhs]

    def multiply(intcode, pos):
        p_lhs, p_rhs, p_dest = intcode[pos + 1], intcode[pos + 2], intcode[pos + 3]
        intcode[p_dest] = intcode[p_lhs] * intcode[p_rhs]

    _intcode = intcode.copy()
    _intcode[1] = noun
    _intcode[2] = verb
    # 1 = add, 2 = multiply, 99 = stop
    instruction_p = 0
    opcode = _intcode[instruction_p]

    while True:
        opcode = _intcode[instruction_p]
        if opcode == 1:
            add(_intcode, instruction_p)
        elif opcode == 2:
            multiply(_intcode, instruction_p)
        elif opcode == 99:
            break
        else:
            raise Exception("invalid opcode")

        instruction_p += 4
        opcode = _intcode[instruction_p]

    return _intcode[0]


intcode = list(map(int, data.split(",")))

# part A
result = program(intcode, 12, 2)

print("Part A result:", result)

# part B
expected_output = 19690720
output = 0
result = 0

for noun in range(100):
    for verb in range(100):
        output = program(intcode, noun, verb)
        if output == expected_output:
            result = 100 * noun + verb
            break

print("Part B result:", result)
