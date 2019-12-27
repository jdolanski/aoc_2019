
def n_to_list_n(n):
    return list(map(int, list(str(n))))


def get_last_good_pos(num_l):
    for i in range(5):
        if num_l[i] > num_l[i+1]:
            return i


min_n = 172930
max_n = 683082
min_l = n_to_list_n(min_n)
last_good_pos = get_last_good_pos(min_l)
for i in range(last_good_pos+1, 6):
    min_l[i] = min_l[last_good_pos]

max_l = n_to_list_n(max_n)
last_good_pos = get_last_good_pos(max_l)
max_l[last_good_pos] = max_l[last_good_pos] - 1
for i in range(last_good_pos+1, 6):
    max_l[i] = 9

min_n = int(''.join(map(str, min_l)))
max_n = int(''.join(map(str, max_l)))


def validate_A(n_l):
    last_seen = n_l[0]
    stack = [last_seen]
    for n in n_l[1:]:
        if last_seen > n:
            return False
        if last_seen != n:
            stack.append(n)
        last_seen = n

    return len(stack) != len(n_l)


def validate_B(n_l):
    last_seen = n_l[0]
    repeat_stack = [0]
    for n in n_l[1:]:
        if last_seen > n:
            return False
        if last_seen != n:
            repeat_stack.append(0)
        else:
            repeat_stack[-1] += 1
        last_seen = n

    return 1 in set(repeat_stack)


# Part A
solutions = 0
for n in range(min_n, max_n+1):
    n_l = n_to_list_n(n)
    if validate_A(n_l):
        solutions += 1
print("Part A solutions:", solutions)

# Part B
solutions = 0
for n in range(min_n, max_n+1):
    n_l = n_to_list_n(n)
    if validate_B(n_l):
        solutions += 1
print("Part B solutions:", solutions)
