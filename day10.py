from aocd import data
import numpy as np
import math

grid = np.array(list(map(
    lambda l: list(map(lambda c: 0 if c == '.' else 1, l)),
    data.split('\n')
)))

# asteroid coordinates
ys, xs = np.where(grid == 1)

# Part A
asteroids_visibility = {}
# LINE EQUATION:
# y - y1 = (y2-y1)/(x2-x1)*(x - x1)
for y1, x1 in zip(ys, xs):
    slopes = set()
    for y2, x2 in zip(ys, xs):
        if y1 == y2 and x1 == x2:
            continue
        dy = y2-y1
        dx = x2-x1
        phi = math.atan2(dy, dx)
        slopes.add(phi)
    asteroids_visibility[(y1, x1)] = len(slopes)

max_k = max(asteroids_visibility, key=asteroids_visibility.get)
print("Part A", asteroids_visibility[max_k])

# Part B
# (y, x) -> [phi -> [(r, (rel_y, rel_x))]]
asteroids_visibility = {}
for y1, x1 in zip(ys, xs):
    slopes_relative_asteroids = {}
    for y2, x2 in zip(ys, xs):
        if y1 == y2 and x1 == x2:
            continue
        dy = y2-y1
        dx = x2-x1
        r = abs(dy) + abs(dx)
        phi = math.atan2(dy, dx)
        rel_asteroids = slopes_relative_asteroids.setdefault(phi, [])
        rel_asteroids.append((r, (y2, x2)))
        slopes_relative_asteroids[phi] = rel_asteroids

    asteroids_visibility[(y1, x1)] = slopes_relative_asteroids

max_k = max(asteroids_visibility, key=lambda k: len(asteroids_visibility[k]))
phi_to_distance_to_coords = asteroids_visibility[max_k]

# the perspective is different because of how 2d arrays are indexed
fourth_q = []
first_second_q = []
third_q = []
# rotate starting from -pi/2 counter-clockwise
for phi in phi_to_distance_to_coords.keys():
    # sort by distance
    vals = sorted(
        phi_to_distance_to_coords[phi], key=lambda x: x[0], reverse=True)
    if phi >= -math.pi/2.0 and phi <= 0:
        fourth_q.append((phi, vals))
    elif phi > 0 and phi <= math.pi:
        first_second_q.append((phi, vals))
    elif phi > -math.pi and phi < -math.pi/2.0:
        third_q.append((phi, vals))

# (phi, [(r, (rel_y, rel_x))])
circle = sorted(fourth_q, key=lambda x: x[0]) + \
    sorted(first_second_q, key=lambda x: x[0]) + \
    sorted(third_q, key=lambda x: x[0])

assert len(circle) == len(phi_to_distance_to_coords)

destroyed_count = 0
last = None
while destroyed_count <= 200:
    for phi, vals in circle:
        if destroyed_count == 200:
            break
        if vals:
            (r, (y, x)) = vals.pop()
            last = (x, y)
            destroyed_count += 1
    else:
        continue
    break

print("Part B", last[0]*100 + last[1])
