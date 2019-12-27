from aocd import data
import numpy as np

# part A
input_list = np.fromiter(data, dtype=np.int)
input_size = input_list.shape[0]

pattern = np.array([0, 1, 0, -1])
pattern_mat = np.empty((input_size, input_size), dtype=int)

for row in range(input_size):
    pattern_mat[row] = np.roll(
        np.tile(np.repeat(pattern, row+1), input_size), -1)[:input_size]

curr_list = input_list.copy()
phases = 100
for i in range(phases):
    z = np.dot(pattern_mat, curr_list)
    curr_list = np.abs(np.fmod(z, 10))

print("Part A", "".join(map(str, curr_list[:8])))

# part B

"""
If the message_offset is more than half the length that means we only need to take in account the digits
after 2nd half of the list. Pattern is upper triangular matrix, the nth digit from the offset is calculated:
    nth_digit = (sum(offset_list[nth_digit:])) mod 10
"""
message_offset = int(data[:7])
input_list = [int(num) for _ in range(10000) for num in data][message_offset:]

for i in range(phases):
    # current_digit = (current_digit + next_digit) mod 10
    # where next_digit is be calculated from previous iteration
    # (n + (m) mod 10) mod 10 = (n + m) mod 10    Identity
    # skip the last element because it will stay the same on each iteration
    for j in range(len(input_list)-2, -1, -1):
        input_list[j] = (input_list[j+1] + input_list[j]) % 10

print("Part B", "".join(map(str, input_list[:8])))
