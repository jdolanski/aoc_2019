from itertools import zip_longest
from collections import deque
from enum import Enum

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

class IntcodeMachine:
    def __init__(self, intcode: list, init_input=[]):
        self.original_intcode = {i: intcode[i] for i in range(0, len(intcode))}
        self.intcode = self.original_intcode.copy()
        self.inputs = deque(init_input)
        self.outputs = deque()
        self.pc = 0
        self.rboffset = 0
        self.waiting_for_input = False
        self.program_completed = False

    def reset(self):
        self.intcode = self.original_intcode.copy()
        self.inputs = deque()
        self.outputs = deque()
        self.pc = 0
        self.rboffset = 0
        self.waiting_for_input = False
        self.program_completed = False

    def clone_state(self):
        # create new machine with current state
        new_machine = IntcodeMachine(self.original_intcode)
        new_machine.intcode = self.intcode.copy()
        new_machine.inputs = self.inputs.copy()
        new_machine.outputs = self.outputs.copy()
        new_machine.pc = self.pc
        new_machine.rboffset = self.rboffset
        new_machine.waiting_for_input = self.waiting_for_input
        new_machine.program_completed = self.program_completed
        
        return new_machine

    def add_input(self, _input):
        self.inputs.append(_input)
        if self.inputs and self.waiting_for_input:
            self.waiting_for_input = False

    def add_inputs(self, _inputs: list):
        self.inputs.extend(_inputs)
        if self.inputs and self.waiting_for_input:
            self.waiting_for_input = False

    def get_output(self):
        if self.outputs:
            out = self.outputs.popleft()
            return out
        else:
            return None

    def run(self):
        while not self.waiting_for_input and not self.program_completed:
            instruction = self.__deref(self.pc)
            opcode = int(instruction[-2:])
            modes = []
            if len(instruction) > 2:
                modes = instruction[0: -2]
            v1, v2, v3 = self.pc+1, self.pc+2, self.pc+3
            if opcode == STORE:
                if not self.inputs:
                    self.waiting_for_input = True
                    break

                _input = self.inputs.popleft()
                if _input is None and not isinstance(_input, int):
                    raise Exception("input must be integer", _input)

                _, dest = self.__eval_params(modes, dest=v1)
                self.intcode[dest] = str(_input)
                self.pc += 1
            elif opcode == OUT:
                [outp], _ = self.__eval_params(modes, ins=[v1])
                self.outputs.append(int(outp))
                self.pc += 1
            elif opcode == SETRB:
                [offset], _ = self.__eval_params(modes, ins=[v1])
                self.rboffset += int(offset)
                self.pc += 1
            elif opcode == ADD:
                [lhs, rhs], dest = self.__eval_params(modes, [v1, v2], dest=v3)
                self.intcode[dest] = str(int(lhs) + int(rhs))
                self.pc += 3
            elif opcode == MUL:
                [lhs, rhs], dest = self.__eval_params(modes, [v1, v2], dest=v3)
                self.intcode[dest] = str(int(lhs) * int(rhs))
                self.pc += 3
            elif opcode == JMPT:
                [val, pointer], _ = self.__eval_params(modes, ins=[v1, v2])
                if val != '0':
                    self.pc = int(pointer)
                    continue
                self.pc += 2
            elif opcode == JMPF:
                [val, pointer], _ = self.__eval_params(modes, ins=[v1, v2])
                if val == '0':
                    self.pc = int(pointer)
                    continue
                self.pc += 2
            elif opcode == LT:
                [lhs, rhs], dest = self.__eval_params(
                    modes, ins=[v1, v2], dest=v3)
                self.intcode[dest] = str(int(int(lhs) < int(rhs)))
                self.pc += 3
            elif opcode == EQ:
                [lhs, rhs], dest = self.__eval_params(
                    modes, ins=[v1, v2], dest=v3)
                self.intcode[dest] = str(int(int(lhs) == int(rhs)))
                self.pc += 3
            elif opcode == END:
                self.program_completed = True
            else:
                raise Exception("invalid opcode", opcode)

            self.pc += 1

        if self.program_completed:
            return 0
        elif self.waiting_for_input:
            return 1

    def __deref(self, addr):
        if addr < 0:
            raise Exception("invalid address", addr)
        return self.intcode.setdefault(addr, '0')

    def __get_value(self, pos, mode):
        return self.__deref(self.__get_index(pos, mode))

    def __get_index(self, pos, mode):
        ipos = int(pos)
        imode = int(mode)
        if imode == POSITION_MODE:
            return int(self.__deref(ipos))
        elif imode == IMMEDIATE_MODE:
            return ipos
        elif imode == RELATIVE_MODE:
            return self.rboffset + int(self.__deref(ipos))
        else:
            raise Exception("invalid mode", imode)

    def __eval_params(self, modes, ins=[], dest=None):
        in_vals = []
        dest_val = None
        n_ins = len(ins)
        revmodes = list(reversed(modes))
        # limit mode sizes for ins
        in_modes = revmodes[:n_ins]
        for param, mode in zip_longest(ins, in_modes, fillvalue='0'):
            in_vals.append(self.__get_value(param, mode))

        if dest:
            dest_mode = POSITION_MODE
            if len(revmodes) > n_ins:
                dest_mode = int(revmodes[n_ins])
            if dest_mode == IMMEDIATE_MODE:
                raise Exception("invalid mode for write parameter", dest_mode)
            dest_val = self.__get_index(dest, dest_mode)

        return in_vals, dest_val
