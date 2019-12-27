from itertools import zip_longest

# MODES
POSITION_MODE = 0
IMMEDIATE_MODE = 1
RELATIVE_MODE = 2

# OPCODES
ADD = 1
MUL = 2
STORE = 3
OUT = 4
JMPT = 5
JMPF = 6
LT = 7
EQ = 8
SETRB = 9
END = 99


def run_eager(_intcode, _inputs=[]):
    inputs = _inputs.copy()
    outs = []
    intcode = {i: _intcode[i] for i in range(0, len(_intcode))}
    pc = 0
    rboffset = 0

    def deref(addr):
        if addr < 0:
            raise Exception("invalid address", addr)
        return intcode.setdefault(addr, '0')

    def get_value(pos, mode):
        return deref(get_index(pos, mode))

    def get_index(pos, mode):
        ipos = int(pos)
        imode = int(mode)
        if imode == POSITION_MODE:
            return int(deref(ipos))
        elif imode == IMMEDIATE_MODE:
            return ipos
        elif imode == RELATIVE_MODE:
            return rboffset + int(deref(ipos))
        else:
            raise Exception("invalid mode", imode)

    def eval_params(modes, ins=[], dest=None):
        in_vals = []
        dest_val = None
        n_ins = len(ins)
        revmodes = list(reversed(modes))
        # limit mode sizes for ins
        in_modes = revmodes[:n_ins]
        for param, mode in zip_longest(ins, in_modes, fillvalue='0'):
            in_vals.append(get_value(param, mode))

        if dest:
            dest_mode = POSITION_MODE
            if len(revmodes) > n_ins:
                dest_mode = int(revmodes[n_ins])
            if dest_mode == IMMEDIATE_MODE:
                raise Exception("invalid mode for write parameter", dest_mode)
            dest_val = get_index(dest, dest_mode)

        return in_vals, dest_val

    while True:
        instruction = deref(pc)
        opcode = int(instruction[-2:])
        modes = []
        if len(instruction) > 2:
            modes = instruction[0: -2]
        v1, v2, v3 = pc+1, pc+2, pc+3

        if opcode == STORE:
            _, dest = eval_params(modes, dest=v1)
            intcode[dest] = str(inputs.pop(0))
            pc += 1
        elif opcode == OUT:
            [outp], _ = eval_params(modes, ins=[v1])
            outs.append(int(outp))
            pc += 1
        elif opcode == SETRB:
            [offset], _ = eval_params(modes, ins=[v1])
            rboffset += int(offset)
            pc += 1
        elif opcode == ADD:
            [lhs, rhs], dest = eval_params(modes, [v1, v2], dest=v3)
            intcode[dest] = str(int(lhs) + int(rhs))
            pc += 3
        elif opcode == MUL:
            [lhs, rhs], dest = eval_params(modes, [v1, v2], dest=v3)
            intcode[dest] = str(int(lhs) * int(rhs))
            pc += 3
        elif opcode == JMPT:
            [val, pointer], _ = eval_params(modes, ins=[v1, v2])
            if val != '0':
                pc = int(pointer)
                continue
            pc += 2
        elif opcode == JMPF:
            [val, pointer], _ = eval_params(modes, ins=[v1, v2])
            if val == '0':
                pc = int(pointer)
                continue
            pc += 2
        elif opcode == LT:
            [lhs, rhs], dest = eval_params(modes, ins=[v1, v2], dest=v3)
            intcode[dest] = str(int(int(lhs) < int(rhs)))
            pc += 3
        elif opcode == EQ:
            [lhs, rhs], dest = eval_params(modes, ins=[v1, v2], dest=v3)
            intcode[dest] = str(int(int(lhs) == int(rhs)))
            pc += 3
        elif opcode == END:
            break
        else:
            raise Exception("invalid opcode", opcode)

        pc += 1

    return outs


def run_lazy(_intcode, init_input=None):
    inputs = [init_input] if init_input else []

    intcode = {i: _intcode[i] for i in range(0, len(_intcode))}
    pc = 0
    rboffset = 0

    def deref(addr):
        if addr < 0:
            raise Exception("invalid address", addr)
        return intcode.setdefault(addr, '0')

    def get_value(pos, mode):
        return deref(get_index(pos, mode))

    def get_index(pos, mode):
        ipos = int(pos)
        imode = int(mode)
        if imode == POSITION_MODE:
            return int(deref(ipos))
        elif imode == IMMEDIATE_MODE:
            return ipos
        elif imode == RELATIVE_MODE:
            return rboffset + int(deref(ipos))
        else:
            raise Exception("invalid mode", imode)

    def eval_params(modes, ins=[], dest=None):
        in_vals = []
        dest_val = None
        n_ins = len(ins)
        revmodes = list(reversed(modes))
        # limit mode sizes for ins
        in_modes = revmodes[:n_ins]
        for param, mode in zip_longest(ins, in_modes, fillvalue='0'):
            in_vals.append(get_value(param, mode))

        if dest:
            dest_mode = POSITION_MODE
            if len(revmodes) > n_ins:
                dest_mode = int(revmodes[n_ins])
            if dest_mode == IMMEDIATE_MODE:
                raise Exception("invalid mode for write parameter", dest_mode)
            dest_val = get_index(dest, dest_mode)

        return in_vals, dest_val

    while True:
        instruction = deref(pc)
        opcode = int(instruction[-2:])
        modes = []
        if len(instruction) > 2:
            modes = instruction[0: -2]
        v1, v2, v3 = pc+1, pc+2, pc+3

        if opcode == STORE:
            if not inputs:
                recv = yield    # wait for input
                inputs.append(recv)
            
            _input = inputs.pop(0)
            if _input is None and not isinstance(_input, int):
                raise Exception("input must be integer", _input)
        
            _, dest = eval_params(modes, dest=v1)
            intcode[dest] = str(_input)
            pc += 1
        elif opcode == OUT:
            [outp], _ = eval_params(modes, ins=[v1])
            yield int(outp)   # push output
            pc += 1
        elif opcode == SETRB:
            [offset], _ = eval_params(modes, ins=[v1])
            rboffset += int(offset)
            pc += 1
        elif opcode == ADD:
            [lhs, rhs], dest = eval_params(modes, [v1, v2], dest=v3)
            intcode[dest] = str(int(lhs) + int(rhs))
            pc += 3
        elif opcode == MUL:
            [lhs, rhs], dest = eval_params(modes, [v1, v2], dest=v3)
            intcode[dest] = str(int(lhs) * int(rhs))
            pc += 3
        elif opcode == JMPT:
            [val, pointer], _ = eval_params(modes, ins=[v1, v2])
            if val != '0':
                pc = int(pointer)
                continue
            pc += 2
        elif opcode == JMPF:
            [val, pointer], _ = eval_params(modes, ins=[v1, v2])
            if val == '0':
                pc = int(pointer)
                continue
            pc += 2
        elif opcode == LT:
            [lhs, rhs], dest = eval_params(modes, ins=[v1, v2], dest=v3)
            intcode[dest] = str(int(int(lhs) < int(rhs)))
            pc += 3
        elif opcode == EQ:
            [lhs, rhs], dest = eval_params(modes, ins=[v1, v2], dest=v3)
            intcode[dest] = str(int(int(lhs) == int(rhs)))
            pc += 3
        elif opcode == END:
            break
        else:
            raise Exception("invalid opcode", opcode)

        pc += 1
