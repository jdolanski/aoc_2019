from aocd import data
import math

# lookup table {chem_name -> (out_amt, {component -> required_amt})}
FORMULAE = {}
for formula_tpl in map(lambda inout: (inout[0].split(", "), inout[1]),
                       map(lambda row: row.split(" => "), data.split('\n'))):
    [components, out] = formula_tpl
    [amt_out, outchem] = out.split(' ')
    inchems = {}
    for component in components:
        [amt_in, inchem] = component.split(' ')
        inchems[inchem] = int(amt_in)
    FORMULAE[outchem] = (int(amt_out), inchems)


# part A


def produce_fuel(needed_amt, curr_formula, stash={}):
    out_amt, components = curr_formula
    times = math.ceil(needed_amt/out_amt)
    ore_spent_accum = 0

    for inchem_name in components:
        component_needed_amt = times * components[inchem_name]
        if inchem_name == 'ORE':
            ore_spent_accum += component_needed_amt
        else:
            stash_amt = stash.setdefault(inchem_name, 0)
            stash[inchem_name] = max(
                stash[inchem_name] - component_needed_amt, 0)
            still_needed_amt = component_needed_amt - stash_amt
            if still_needed_amt > 0:
                inchem_formula = FORMULAE[inchem_name]
                produced, ore_spent = produce_fuel(
                    still_needed_amt, inchem_formula, stash)
                stash[inchem_name] += produced - still_needed_amt
                ore_spent_accum += ore_spent

    return (times * out_amt, ore_spent_accum)


_, ore_spent = produce_fuel(1, FORMULAE['FUEL'])

print("Part A", ore_spent)

# part B
TOTAL_AVAILABLE_ORE = 1000000000000


def produce_fuel_limited_ore(needed_amt, curr_formula, stash={}):
    out_amt, components = curr_formula
    times = math.ceil(needed_amt/out_amt)

    for inchem_name in components:
        component_needed_amt = times * components[inchem_name]
        if inchem_name == 'ORE':
            stash['ORE'] -= component_needed_amt
            if stash['ORE'] < 0:
                return -1
        else:
            stash_amt = stash.setdefault(inchem_name, 0)
            stash[inchem_name] = max(
                stash[inchem_name] - component_needed_amt, 0)
            still_needed_amt = component_needed_amt - stash_amt
            if still_needed_amt > 0:
                inchem_formula = FORMULAE[inchem_name]
                produced = produce_fuel_limited_ore(
                    still_needed_amt, inchem_formula, stash)
                if produced == -1:
                    return -1
                stash[inchem_name] += produced - still_needed_amt

    return times * out_amt


def binsearch(min_fuel, max_fuel):
    if max_fuel > min_fuel:
        mid = min_fuel + int((max_fuel - min_fuel) / 2)
        produced = produce_fuel_limited_ore(
            mid, FORMULAE['FUEL'], {'ORE': TOTAL_AVAILABLE_ORE})
        if produced == -1:
            return binsearch(min_fuel, mid - 1)
        else:
            return binsearch(mid + 1, max_fuel)
    else:
        return max_fuel


max_fuel = binsearch(0, TOTAL_AVAILABLE_ORE)

print("Part B", max_fuel)
