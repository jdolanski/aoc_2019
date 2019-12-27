from aocd import data
import numpy as np

rows = data.split("\n")
xyz = []
for row in rows:
    x, y, z = row[1:-1].split(",")
    xyz.append((int(x[2:]), int(y[3:]), int(z[3:])))

# part A
moons_pos = np.asarray(xyz)
n_moons, _ = moons_pos.shape
velocities = np.zeros_like(moons_pos)
next_pos = np.zeros_like(moons_pos)

for _ in range(1000):
    for j in range(n_moons):
        moon = moons_pos[j]
        acceleration = np.clip(moons_pos - moon, -1, 1)
        velocities[j] += np.sum(acceleration, axis=0)
        next_pos[j] = moon + velocities[j]

    moons_pos = np.copy(next_pos)

potential = np.sum(np.abs(moons_pos), axis=1)
kinetic = np.sum(np.abs(velocities), axis=1)
total = np.sum(np.multiply(potential, kinetic))
print("Part A", total)

# part B
moons_pos = np.asarray(xyz)
n_moons, _ = moons_pos.shape
velocities = np.zeros_like(moons_pos)
next_pos = np.zeros_like(moons_pos)

time = 0
axes_records = ({}, {}, {})
freqs = [0, 0, 0]
while not(all(freqs)):
    def record_axis_step(axis):
        if not freqs[axis]:
            points = tuple(np.concatenate(
                (moons_pos[:, axis], velocities[:, axis])))
            prev_time = axes_records[axis].setdefault(points, time)
            dtime = time - prev_time
            if dtime > 0:
                freqs[axis] = dtime

    record_axis_step(0)
    record_axis_step(1)
    record_axis_step(2)

    for i in range(n_moons):
        moon = moons_pos[i]
        acceleration = np.clip(moons_pos - moon, -1, 1)
        velocities[i] += np.sum(acceleration, axis=0)
        next_pos[i] = moon + velocities[i]

    moons_pos = np.copy(next_pos)
    time += 1

steps_needed = np.lcm.reduce(freqs)
print("Part B", steps_needed)
