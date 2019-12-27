from aocd import data
from collections import deque
from intcode_machine_new import IntcodeMachine


# part A
intcode = data.split(',')

computers = []
for address in range(50):
    c = IntcodeMachine(intcode, [address, -1])
    c.run()
    computers.append(c)

result = None
packets_queue = deque([], maxlen=50)
while True:
    packet = (None, None, None)
    if packets_queue:
        packet = packets_queue.popleft()

    if packet[0] == 255:
        result = packet[2]
        break

    for address in range(50):
        computer = computers[address]
        ADDR = computer.get_output()
        if ADDR is not None:
            X = computer.get_output()
            Y = computer.get_output()
            packets_queue.append((ADDR, X, Y))

        if packet[0] == address:
            computer.add_inputs([packet[1], packet[2]])
        else:
            computer.add_input(-1)

        computer.run()


print("Part A", result)

# part B
intcode = data.split(',')

computers = []
for address in range(50):
    c = IntcodeMachine(intcode, [address, -1])
    c.run()
    computers.append(c)

result = None
NAT = {
    'current': (None, None),
    'last_sent': (None, None)
}
packets_queue = deque([], maxlen=50)
while True:
    packet = (None, None, None)
    if packets_queue:
        packet = packets_queue.popleft()

    if packet[0] == 255:
        NAT['current'] = (packet[1], packet[2])

    idle = True
    for address in range(50):
        computer = computers[address]
        ADDR = computer.get_output()
        if ADDR is not None:
            idle = False
            X = computer.get_output()
            Y = computer.get_output()
            packets_queue.append((ADDR, X, Y))

        if packet[0] == address:
            idle = False
            computer.add_inputs([packet[1], packet[2]])
        else:
            computer.add_input(-1)

        computer.run()

    if idle:
        X, Y = NAT['current']

        if Y == NAT['last_sent'][1]:
            result = Y
            break

        NAT['last_sent'] = (X, Y)
        computer = computers[0]
        computer.add_inputs([X, Y])
        computer.run()


print("Part B", result)
