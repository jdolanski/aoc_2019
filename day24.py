from aocd import data
import numpy as np
from collections import defaultdict
import datetime

# part A
arr = np.array(list(map(lambda str: list(
    map(lambda c: 0 if c == '.' else 1, str)), data.split('\n'))), dtype=np.int8)
h, w = arr.shape

bugmask = np.zeros_like(arr)
biodiversity_ratings = set()
biodiversity_mask = 2 ** np.arange(0, h*w).reshape(h, w)
result = 0
while True:
    rr = -1, 1, 0, 0
    cc = 0, 0, 1, -1
    for y in range(h):
        for x in range(w):
            for i in range(4):
                ny, nx = y+rr[i], x+cc[i]
                if 0 <= ny < h and 0 <= nx < w:
                    bugmask[y, x] += arr[ny, nx]

    for y in range(h):
        for x in range(w):
            count = bugmask[y, x]
            bug = arr[y, x]
            if not bug and (count == 1 or count == 2):
                arr[y, x] = 1
            elif not(bug and count == 1):
                arr[y, x] = 0

    rating = np.sum(
        np.sum(np.multiply(arr, biodiversity_mask)))
    if rating in biodiversity_ratings:
        result = rating
        break

    biodiversity_ratings.add(rating)
    bugmask.fill(0)

print("Part A", result)

# part B
arr = np.array(list(map(lambda str: list(
    map(lambda c: 1 if c == '#' else 0, str)), data.split('\n'))), dtype=np.int8)
h, w = arr.shape

layers = defaultdict(lambda: np.zeros_like(arr), {0: arr})
bugmasks = defaultdict(lambda: np.zeros_like(arr), {0: np.zeros_like(arr)})
rr = -1, 1, 0, 0
cc = 0, 0, 1, -1
for _ in range(200):
    for layern in range(min(layers) - 1, max(layers) + 2):
        bugmask = bugmasks[layern]
        current = layers[layern]
        inner = layers[layern-1]
        outer = layers[layern+1]
        for y in range(h):
            for x in range(w):
                if y == 2 and x == 2:
                    continue
                for i in range(4):
                    ny, nx = y+rr[i], x+cc[i]
                    if ny == -1:
                        # inner upper of layer-1
                        bugmask[y, x] += inner[1, 2]
                    elif ny == h:
                        # inner bottom of layer-1
                        bugmask[y, x] += inner[3, 2]
                    elif nx == -1:
                        # inner left of layer-1
                        bugmask[y, x] += inner[2, 1]
                    elif nx == w:
                        # inner right of layer-1
                        bugmask[y, x] += inner[2, 3]
                    elif ny == 2 and nx == 2:
                        # get outer sides of layer+1
                        outer = layers[layern+1]
                        if y == 1 and x == 2:
                            # outer upper of layer+1
                            bugmask[y, x] += np.sum(outer[0])
                        elif y == 2 and x == 1:
                            # outer left of layer+1
                            bugmask[y, x] += np.sum(outer[:, 0])
                        elif y == 2 and x == 3:
                            # outer right of layer+1
                            bugmask[y, x] += np.sum(outer[:, -1])
                        elif y == 3 and x == 2:
                            # outer bottom of layer+1
                            bugmask[y, x] += np.sum(outer[-1])
                    else:
                        bugmask[y, x] += current[ny, nx]

    for layern in range(min(layers) - 1, max(layers) + 2):
        bugmask = bugmasks[layern]
        current_layer = layers[layern]
        for y in range(h):
            for x in range(w):
                count = bugmask[y, x]
                bug = current_layer[y, x]
                if not bug and (count == 1 or count == 2):
                    current_layer[y, x] = 1
                elif not(bug and count == 1):
                    current_layer[y, x] = 0

        bugmask.fill(0)
        if np.count_nonzero(current_layer) == 0:
            del layers[layern]

total_bugs = 0
for layer in layers.values():
    total_bugs += layer.sum()

print("Part B", total_bugs)
