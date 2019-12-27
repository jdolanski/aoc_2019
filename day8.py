from aocd import data
import itertools
import numpy as np
import textwrap

pixels = data
h = 6
w = 25
step = h*w

# Part A
min0s21sx2s = ()
for idx in range(0, len(pixels), step):
    layer = pixels[idx:idx+step]
    c = layer.count('0')
    if not min0s21sx2s or min0s21sx2s[0] > c:
        min0s21sx2s = (c, layer.count('1')*layer.count('2'))

print("Part A", min0s21sx2s[1])

# Part B
final_img = list(pixels[0:step])
for idx in range(step, len(pixels), step):
    layer = pixels[idx:idx+step]
    for i, (fp, lp) in enumerate(zip(final_img, layer)):
        if fp == '2':
            final_img[i] = lp

message = textwrap.fill(
    "".join(map(lambda c: '*' if c == '1' else '.', final_img)), w)

print("Part B")
print(message)
