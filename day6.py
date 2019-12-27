from aocd import data

orbits = data.split("\n")
c_to_o = list(map(lambda o: o.split(")"), orbits))
orbital_graph = {}
for orbited, orbiter in c_to_o:
    orbital_graph[orbiter] = orbited

# Part A


def search(orbiter, graph, count):
    orbited = graph.get(orbiter)
    if not orbited:
        return count
    else:
        return search(orbited, graph, count + 1)


total_count = 0
for orbiter in orbital_graph.keys():
    orbited = orbital_graph.get(orbiter)
    if orbited:
        count = search(orbited, orbital_graph, 1)
        total_count += count

print("Part A", total_count)

# Part B


def search_accum_san(orbiter, graph, count, san_accum):
    san_accum[orbiter] = count
    orbited = graph.get(orbiter)
    if not orbited:
        return san_accum
    else:
        return search_accum_san(orbited, graph, count + 1, san_accum)


def find_steps_to_closest_parent(orbiter, graph, count, you_accum, san_accum):
    you_accum[orbiter] = count
    orbited = graph[orbiter]
    if orbited in san_accum:
        san_count = san_accum[orbited]
        return count + san_count + 1
    else:
        return find_steps_to_closest_parent(orbited, graph, count + 1, you_accum, san_accum)


SAN_O = orbital_graph['SAN']
YOU_O = orbital_graph['YOU']
you_count_per_obj = find_steps_to_closest_parent(
    YOU_O, orbital_graph, 0, {},
    search_accum_san(SAN_O, orbital_graph, 0, {})
)

print("Part B", you_count_per_obj)
