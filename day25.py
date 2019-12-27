from aocd import data
from collections import deque
from intcode_machine_new import IntcodeMachine


def flush_out(robot):
    string = "".join(map(chr, robot.outputs))
    robot.outputs.clear()
    return string


intcode = data.split(',')
robot = IntcodeMachine(intcode)
robot.run()
while True:
    prompt = flush_out(robot)
    if not prompt:
        break
    print(prompt)

    userinput = input()
    normalizedinput = userinput.lower().strip()
    gameinput = None
    if normalizedinput == "west" or normalizedinput == "h":
        gameinput = "west"
    elif normalizedinput == "south" or normalizedinput == "j":
        gameinput = "south"
    elif normalizedinput == "north" or normalizedinput == "k":
        gameinput = "north"
    elif normalizedinput == "east" or normalizedinput == "l":
        gameinput = "east"
    elif normalizedinput.startswith("take") or normalizedinput.startswith("g"):
        item = " ".join(normalizedinput.split(" ")[1:])
        gameinput = "take " + item
    elif normalizedinput.startswith("drop") or normalizedinput.startswith("d"):
        item = " ".join(normalizedinput.split(" ")[1:])
        gameinput = "drop " + item
    elif normalizedinput == "inv" or normalizedinput == "i":
        gameinput = "inv"

    asciiinput = list(map(ord, list(gameinput))) + [ord('\n')]
    robot.add_inputs(asciiinput)
    robot.run()
