from queue import PriorityQueue
import math

in_path = 'testcases/input1.txt'
out_path = 'output.txt'

size = []
landing = []
targets = []
area = []
num_targets = 0
max_elevation = 0


# class Node:
#     def __init__(self, coordinates, value, parent=None, cost=0):
#         self.coordinates = coordinates
#         self.parent = parent
#         self.cost = cost
#         self.value = value


def check_valid_neighbors(x, y, grid, z, visited, parent):
    valid_neighbors = []
    # up
    if x - 1 >= 0 and abs(grid[x - 1][y] - grid[x][y]) <= z and [x - 1, y] not in visited:
        valid_neighbors.append([x - 1, y])
        parent[str(x - 1) + ',' + str(y)] = [x, y]
    # down
    if x + 1 < len(grid) and abs(grid[x + 1][y] - grid[x][y]) <= z and [x + 1, y] not in visited:
        valid_neighbors.append([x + 1, y])
        parent[str(x + 1) + ',' + str(y)] = [x, y]
    # left
    if y - 1 >= 0 and abs(grid[x][y - 1] - grid[x][y]) <= z and [x, y - 1] not in visited:
        valid_neighbors.append([x, y - 1])
        parent[str(x) + ',' + str(y - 1)] = [x, y]
    # right
    if y + 1 < len(grid[0]) and abs(grid[x][y + 1] - grid[x][y]) <= z and [x, y + 1] not in visited:
        valid_neighbors.append([x, y + 1])
        parent[str(x) + ',' + str(y + 1)] = [x, y]

    # top-left
    if x - 1 >= 0 and y - 1 >= 0 and abs(grid[x - 1][y - 1] - grid[x][y]) <= z and [x - 1, y - 1] not in visited:
        valid_neighbors.append([x - 1, y - 1])
        parent[str(x - 1) + ',' + str(y - 1)] = [x, y]
    # top-right
    if x - 1 >= 0 and y + 1 < len(grid[0]) and abs(grid[x - 1][y + 1] - grid[x][y]) <= z and [x - 1,
                                                                                              y + 1] not in visited:
        valid_neighbors.append([x - 1, y + 1])
        parent[str(x - 1) + ',' + str(y + 1)] = [x, y]
    # bottom-left
    if x + 1 < len(grid) and y - 1 >= 0 and abs(grid[x + 1][y - 1] - grid[x][y]) <= z and [x + 1, y - 1] not in visited:
        valid_neighbors.append([x + 1, y - 1])
        parent[str(x + 1) + ',' + str(y - 1)] = [x, y]
    # bottom-right
    if x + 1 < len(grid) and y + 1 < len(grid[0]) and abs(grid[x + 1][y + 1] - grid[x][y]) <= z and [x + 1,
                                                                                                     y + 1] not in visited:
        valid_neighbors.append([x + 1, y + 1])
        parent[str(x + 1) + ',' + str(y + 1)] = [x, y]

    return valid_neighbors


# implement
def bfs(start, territory, targets, z):
    parent = {}
    explored = []
    targets_found = []
    q = [start]

    while q and len(targets_found) != len(targets):
        [x, y] = q.pop(0)
        explored.append([x, y])
        if [x, y] in targets:
            targets_found.append([x, y])

        q.extend(check_valid_neighbors(x, y, territory, z, explored, parent))  # pushing all the valid neighbors

    paths = []

    for target in targets_found:
        temp_path = []

        curr = target

        while curr != start:
            temp_path.append(curr)
            curr = parent[str(curr[0]) + ',' + str(curr[1])]
        temp_path.append(start)

        paths.append(temp_path)

    path_string = ""

    for path in paths:
        for coors in path:
            temp = str(coors[1]) + ',' + str(coors[0]) + ' '
            path_string += temp
        path_string += '\n'
    path_string = path_string.strip()

    with open(out_path, 'w') as op:
        if path_string:
            op.write(path_string)
        else:
            op.write('FAIL')


def distance_2D(x1, y1, x2, y2):
    return math.sqrt(pow(x2 - x1, 2) + pow(y2 - y1, 2))


# once you get children loop over the list of children and calculating the cost => parent_cost + 2D_distance(parent, child)
# bfs => [x,y] im queue; ucs => [cost, [x ,y]]

def ucs(start, territory, targets, z):
    # start_node = Node(start, territory[start[0]][start[1]])

    qopen = PriorityQueue()

    # open.put(0, start_node)
    qopen.put((0, start, [start]))
    visited = []
    parent = {}
    path = []
    main_path = []
    # targets_found = []
    while not qopen.empty():
        parent_cost, curr, path = qopen.get()
        visited.append(curr)
        # print(targets)
        if curr in targets:
            targets.remove(curr)
            main_path.append(path)
            # print(path)
            if targets == []:
                break
        curr_children = check_valid_neighbors(curr[0], curr[1], territory, z, visited, parent)
        # print(curr, curr_children)
        for child in curr_children:
            cost = parent_cost + distance_2D(child[0], child[1], curr[0], curr[1])
            qopen.put((cost, child, path + [child]))
            # print(child, cost)

    path_string = ''
    for path in main_path:
        for p in path:
            temp = str(p[1]) + ',' + str(p[0]) + ' '
            path_string += temp
        path_string += '\n'
        path_string = path_string.strip()
    # print(path_string)

    with open(out_path, 'w') as op:
        if path_string:
            op.write(path_string)
        else:
            op.write('FAIL')

        #
        # while curr_children:
        #     child = open.get()
        #     if child not in open or child not in closed:
        #         open.put(cost, [cost, child])
        #     elif child in open:
        #         if


def aStar(start, territory, targets, z):
    # targets_found = []
    main_path = []
    for target in targets:
        qopen = PriorityQueue()

        # open.put(0, start_node)
        qopen.put((0, start, [start]))
        visited = []
        parent = {}
        path = []

        while not qopen.empty():
            parent_cost, curr, path = qopen.get()
            visited.append(curr)
            if curr == target:
                main_path.append(path)
                break
            curr_children = check_valid_neighbors(curr[0], curr[1], territory, z, visited, parent)
            # print(curr, curr_children)
            for child in curr_children:
                cost = parent_cost + distance_2D(child[0], child[1], curr[0], curr[1]) + distance_2D(child[0], child[1], \
                                                                                                     target[0],
                                                                                                     target[1]) + abs(
                    territory[curr[0]][curr[1]] - territory[child[0]][child[1]])
                qopen.put((cost, child, path + [child]))
                # print(child, cost)
    path_string = ''
    for path in main_path:
        for p in path:
            temp = str(p[1]) + ',' + str(p[0]) + ' '
            path_string += temp
        path_string += '\n'
        path_string = path_string.strip()
    # print(path_string)

    with open(out_path, 'w') as op:
        if path_string:
            op.write(path_string)
        else:
            op.write('FAIL')


'''Open the file and read inputs'''

try:
    with open(in_path, 'r') as inp, open(out_path, 'w') as op:
        algorithm = inp.readline().rstrip('\n')
        '''Read the string and split it to integers. map to convert the items of iterables to built-ins like int, float,
        str. In Python 3, map will return a lazy object, convert into a list with list() '''
        size = list(map(int, inp.readline().split()))
        temp_landing = list(map(int, inp.readline().split()))
        landing = temp_landing[::-1]
        # print(landing)
        max_elevation = int(inp.readline())
        num_targets = int(inp.readline())
        for i in range(num_targets):
            temp_list = list(map(int, inp.readline().split()))
            targets.append(temp_list[::-1])
            # targets.append(list(map(int, inp.readline().split())))
        for i in range(size[1]):
            area.append(list(map(int, inp.readline().split())))

        # print(targets)
        if algorithm == 'BFS':
            #print('BFS')
            # BFS logic goes here
            bfs(landing, area, targets, max_elevation)
        elif algorithm == 'UCS':
            #print('UCS')
            # UCS logic goes here
            ucs(landing, area, targets, max_elevation)
        elif algorithm == 'A*':
            #print("A*")
            # A* logic goes here
            aStar(landing, area, targets, max_elevation)
        else:
            op.write("FAIL")
except IOError:
    op.write("FAIL")

    # print(algorithm)
    # print(size)
    # print(landing)
    # print(max_elevation)
    # print(num_targets)
    # print(targets)
