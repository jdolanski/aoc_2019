from aocd import data
from collections import deque

test1 = """
         A           
         A           
  #######.#########  
  #######.........#  
  #######.#######.#  
  #######.#######.#  
  #######.#######.#  
  #####  B    ###.#  
BC...##  C    ###.#  
  ##.##       ###.#  
  ##...DE  F  ###.#  
  #####    G  ###.#  
  #########.#####.#  
DE..#######...###.#  
  #.#########.###.#  
FG..#########.....#  
  ###########.#####  
             Z       
             Z       """.lstrip('\n')

test2 = """
                   A               
                   A               
  #################.#############  
  #.#...#...................#.#.#  
  #.#.#.###.###.###.#########.#.#  
  #.#.#.......#...#.....#.#.#...#  
  #.#########.###.#####.#.#.###.#  
  #.............#.#.....#.......#  
  ###.###########.###.#####.#.#.#  
  #.....#        A   C    #.#.#.#  
  #######        S   P    #####.#  
  #.#...#                 #......VT
  #.#.#.#                 #.#####  
  #...#.#               YN....#.#  
  #.###.#                 #####.#  
DI....#.#                 #.....#  
  #####.#                 #.###.#  
ZZ......#               QG....#..AS
  ###.###                 #######  
JO..#.#.#                 #.....#  
  #.#.#.#                 ###.#.#  
  #...#..DI             BU....#..LF
  #####.#                 #.#####  
YN......#               VT..#....QG
  #.###.#                 #.###.#  
  #.#...#                 #.....#  
  ###.###    J L     J    #.#.###  
  #.....#    O F     P    #.#...#  
  #.###.#####.#.#####.#####.###.#  
  #...#.#.#...#.....#.....#.#...#  
  #.#####.###.###.#.#.#########.#  
  #...#.#.....#...#.#.#.#.....#.#  
  #.###.#####.###.###.#.#.#######  
  #.#.........#...#.............#  
  #########.###.###.#############  
           B   J   C               
           U   P   P               """.lstrip('\n')

test3 = """
             Z L X W       C                 
             Z P Q B       K                 
  ###########.#.#.#.#######.###############  
  #...#.......#.#.......#.#.......#.#.#...#  
  ###.#.#.#.#.#.#.#.###.#.#.#######.#.#.###  
  #.#...#.#.#...#.#.#...#...#...#.#.......#  
  #.###.#######.###.###.#.###.###.#.#######  
  #...#.......#.#...#...#.............#...#  
  #.#########.#######.#.#######.#######.###  
  #...#.#    F       R I       Z    #.#.#.#  
  #.###.#    D       E C       H    #.#.#.#  
  #.#...#                           #...#.#  
  #.###.#                           #.###.#  
  #.#....OA                       WB..#.#..ZH
  #.###.#                           #.#.#.#  
CJ......#                           #.....#  
  #######                           #######  
  #.#....CK                         #......IC
  #.###.#                           #.###.#  
  #.....#                           #...#.#  
  ###.###                           #.#.#.#  
XF....#.#                         RF..#.#.#  
  #####.#                           #######  
  #......CJ                       NM..#...#  
  ###.#.#                           #.###.#  
RE....#.#                           #......RF
  ###.###        X   X       L      #.#.#.#  
  #.....#        F   Q       P      #.#.#.#  
  ###.###########.###.#######.#########.###  
  #.....#...#.....#.......#...#.....#.#...#  
  #####.#.###.#######.#######.###.###.#.#.#  
  #.......#.......#.#.#.#.#...#...#...#.#.#  
  #####.###.#####.#.#.#.#.###.###.#.###.###  
  #.......#.....#.#...#...............#...#  
  #############.#.#.###.###################  
               A O F   N                     
               A A D   M                     """.lstrip('\n')


def print_maze(maze, modifications={}):
    _maze = maze.copy()
    for mod in modifications:
        _maze[mod[0]] = _maze[mod[0]][:mod[1]] + \
            modifications[mod] + _maze[mod[0]][mod[1]+1:]
    for row in _maze:
        print(row)


def get_portals(maze):
    h, w = len(maze), len(maze[0])
    starty, startx, endy, endx = None, None, None, None
    for i in range(2, h-2):
        if endx is None:
            start = 2
            if startx is not None:
                start = startx
            for j in range(start, w-2):
                if startx is None and starty is None and maze[i][j] == ' ':
                    starty, startx = i, j
                elif startx is not None and starty is not None and endx is None and maze[i][j] == '#':
                    endx = j
        else:
            if maze[i][endx-1] == '#':
                endy = i
                break

    portal_coord_to_portal = {}
    portal_to_coords = {}
    start_end = [None, None]
    portal_coord_isinner = {}

    def isportal(p):
        return len(p) == 2 and p.isupper()

    def update_portals(p, y, x, isinner):
        if p == 'AA':
            start_end[0] = (y, x)
        elif p == 'ZZ':
            start_end[1] = (y, x)
        else:
            portal_coord_to_portal[(y, x)] = p
            portal_to_coords.setdefault(p, set())
            portal_to_coords[p].add((y, x))
            portal_coord_isinner[(y, x)] = isinner

    # horizontal portals
    for i, r in enumerate(maze[2:h-2]):
        y = i + 2
        # outer left
        p1 = r[0:2].strip()
        if isportal(p1):
            x = 2
            update_portals(p1, y, x, False)
        # inner left
        p2 = r[startx:startx+2].strip()
        if isportal(p2):
            x = startx-1
            update_portals(p2, y, x, True)
        # inner right
        p3 = r[endx-2:endx].strip()
        if isportal(p3):
            x = endx
            update_portals(p3, y, x, True)
        # outer right
        p4 = r[w-2:w].strip()
        if isportal(p4):
            x = w-3
            update_portals(p4, y, x, False)
    # vertical portals
    for i in range(2, w-2):
        x = i
        # outer top
        p1 = (maze[0][i] + maze[1][i]).strip()
        if isportal(p1):
            y = 2
            update_portals(p1, y, x, False)
        # inner top
        p2 = (maze[starty][i] + maze[starty+1][i]).strip()
        if isportal(p2):
            y = starty-1
            update_portals(p2, y, x, True)
        # inner bottom
        p3 = (maze[endy-2][i] + maze[endy-1][i]).strip()
        if isportal(p3):
            y = endy
            update_portals(p3, y, x, True)
        # outer bottom
        p4 = (maze[h-2][i] + maze[h-1][i]).strip()
        if isportal(p4):
            y = h-3
            update_portals(p4, y, x, False)

    return start_end[0], start_end[1], portal_coord_to_portal, portal_to_coords, portal_coord_isinner


maze = data.split('\n')
# startyx, endyx, {y, x -> name}, {name -> {(y, x)}}, {y, x -> isinner}
ports = get_portals(maze)
AA, ZZ, portal_coord_to_portal, portal_to_coords, portal_coord_isinner = ports
# draw maze with the portal locations
mods = {}
for p in portal_coord_to_portal:
    mods[p] = '∆'
mods[AA] = '@'
mods[ZZ] = '>'
print_maze(maze, mods)

# part A


def bfs_portals(maze, AA, ZZ, portal_coord_to_portal, portal_to_coords):
    queue = deque([(AA, False), None])
    visited = set([AA])
    steps = 0

    while queue:
        elem = queue.popleft()
        if elem is None:
            steps += 1
            queue.append(None)
            if queue[0] is None:
                break
            else:
                continue

        curr_yx, portaled = elem

        if curr_yx == ZZ:
            break
        elif not portaled and curr_yx in portal_coord_to_portal:
            portal = portal_coord_to_portal[curr_yx]
            portal_end_yx = list(portal_to_coords[portal] - {curr_yx})[0]
            visited.add(portal_end_yx)
            queue.append((portal_end_yx, True))
        else:
            for r, c in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
                new_yx = (curr_yx[0]+r, curr_yx[1]+c)
                cell = maze[new_yx[0]][new_yx[1]]

                if new_yx not in visited and cell == '.':
                    visited.add(new_yx)
                    queue.append((new_yx, False))

    return steps


steps = bfs_portals(maze, AA, ZZ, portal_coord_to_portal, portal_to_coords)

print("Part A", steps)

# part B


def bfs_3d_maze(maze, AA, ZZ, portal_coord_to_portal, portal_to_coords, portal_coord_isinner):
    # node, level, portaled
    queue = deque([(AA, 0, False), None])
    visited_at_level = {0: set([AA])}
    steps = 0

    while queue:
        elem = queue.popleft()
        if elem is None:
            steps += 1
            queue.append(None)
            if queue[0] is None:
                break
            else:
                continue

        curr_yx, level, portaled = elem

        if curr_yx == ZZ and level == 0:
            break
        elif (not portaled
              and curr_yx in portal_coord_to_portal
              and (level > 0 or portal_coord_isinner[curr_yx] == True)):
            portal = portal_coord_to_portal[curr_yx]
            isinner = portal_coord_isinner[curr_yx]
            new_level = level + 1 if isinner else level - 1
            portal_end_yx = list(portal_to_coords[portal] - {curr_yx})[0]

            visited_at_level.setdefault(new_level, set())
            visited_at_level[new_level].add(portal_end_yx)
            queue.append((portal_end_yx, new_level, True))
        else:
            for r, c in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
                new_yx = (curr_yx[0]+r, curr_yx[1]+c)
                cell = maze[new_yx[0]][new_yx[1]]

                if new_yx not in visited_at_level[level] and cell == '.':
                    visited_at_level[level].add(new_yx)
                    queue.append((new_yx, level, False))

    return steps


steps = bfs_3d_maze(maze, AA, ZZ, portal_coord_to_portal,
                    portal_to_coords, portal_coord_isinner)

print("Part B", steps)
