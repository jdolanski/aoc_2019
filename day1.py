import numpy as np
from aocd import data


def calculate_fuel(mass_arr):
    def required_fuel(_mass_arr): return np.clip(
        _mass_arr // 3 - 2, a_min=0, a_max=None)

    def calculate(fuel_arr):
        f_arr = required_fuel(fuel_arr)
        if np.count_nonzero(f_arr) == 0:
            return fuel_arr
        else:
            return fuel_arr + calculate(f_arr)

    fuel_arr = required_fuel(mass_arr)
    return calculate(fuel_arr)


masses = np.asarray(list(map(int, data.splitlines())))

total_required_fuel = np.sum(calculate_fuel(masses))
print("Required fuel:", total_required_fuel)
