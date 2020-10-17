import time

def bfs(maze):
    return

def dfs(maze):
    return

def best_first(maze):
    return

def hill_climbing(maze):
    return

class Node:
        def __init__(self, parent = None, position = None):
            self.parent = parent
            self.position = position

            self.costToCurr = 0
            self.heuristic = 0
            self.totalCost = 0

        def __eq__ (self, other):
            return self.position == other.position

def return_path(current_node, maze):
    path = []

    result = [[-1 for i in range(len(maze.board))] for j in range(len(maze.board[0]))]
    current = current_node

    while current is not None:
        path.append(current.position)
        current = current.parent

    path = path[:: -1]
    start_value = 0

    for i in range(len(path)):
        result[path[i][0]][path[i][1]] = start_value
        start_value += 1
    
    return result
#! change to manhattan distance
def heuristic(child, end):
    return (((child.position[0] - end.position[0]) ** 2) +
            ((child.position[1] - end.position[1]) ** 2))

def a_star(maze):
    # initialize start node
    start_node = Node(None, tuple(maze.spawn))
    start_node.costToCurr = start_node.heuristic = start_node.totalCost = 0
    # initialize end node
    end_node = Node(None, tuple(maze.end))
    end_node.costToCurr = end_node.heuristic = end_node.totalCost = 0

    yet_to_visit = []
    visited = []

    yet_to_visit.append(start_node)

    outer_iterations = 0
    max_iterations = (len(maze.board) // 2) ** 10


    move = [[-1,0], #up
            [0,-1],  #left
            [1,0],  #down
            [0,1]]  #right

    while len(yet_to_visit) > 0:
        print(len(yet_to_visit))
        outer_iterations += 1

        #get current node
        current_node = yet_to_visit[0]
        current_index = 0
        for index, item in enumerate(yet_to_visit):
            if item.totalCost < current_node.totalCost:
                current_node = item
                current_index = index

        if outer_iterations > max_iterations:
            print("giving up on patfinding too many iterations")
            return return_path(current_node, maze)
        
        yet_to_visit.pop(current_index)
        visited.append(current_node)
        print(current_node)
        if current_node == end_node:
            return return_path(current_node, maze)
        
        children = []

        for new_position in move:
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            if(node_position[0] > (len(maze.board) - 1) or
                node_position[0] < 0 or
                node_position[1] > (len(maze.board[0]) - 1) or
                node_position[1] < 0):
                continue

            if maze.board[node_position[0]][node_position[1]] != "*":
                continue

            new_node = Node(current_node, node_position)

            children.append(new_node)

        for child in children:
            if len([visited_child for visited_child in visited if visited_child == child]) > 0:
                continue

            child.costToCurr = current_node.costToCurr + maze.cost

            child.heuristic = heuristic(child, end_node)

            child.totalCost = child.costToCurr + child.heuristic

            if len([i for i in yet_to_visit if child == i and child.costToCurr > i.costToCurr]) > 0:
                continue

            yet_to_visit.append(child)

class Maze:
    def __init__(self, x, y):
        self.board = [[None for _ in range(y)] for _ in range(x)]
        self.spawn = []
        self.end = []
        self.cost = 1
        self.solution = []

    def print(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                print(self.board[i][j], end=' ')
            print()

#===================================#

shape = input().split()
x = int(shape[0])
y = int(shape[1])

maze = Maze(x, y)

for i in range(x):
    line = [char for char in input() if char != '\r']
    for j in range(len(line)):
        if line[j] == "#":
            maze.spawn = i, j
        elif line[j] == "$":
            maze.end = i, j
        maze.board[i][j] = line[j]
        

# bfs(maze)
# dfs(maze)
# best_first(maze)
path = a_star(maze)
print(path)
# hill_climbing(maze)