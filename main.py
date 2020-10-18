import time

def bfs(maze):
    return

def dfs(maze):
    return


def hill_climbing(maze):
    return

# Class that represents a node
class Node:
    def __init__(self, parent = None, position = None):
        self.parent = parent
        self.position = position

        self.g = 0 #distance to start node
        self.h = 0 #distance to goal node
        self.f = 0 #total cost

    #compare nodes
    def __eq__ (self, other):
        return self.position == other.position
    # sort nodes
    def __lt__ (self, other):
        return self.f < other.f


#Manhattan distance used in A* heuristic
def heuristic(current, end):
    return ((abs(current.position[0] - end.position[0])) + (abs(current.position[1] - end.position[1])))

#Best First Search
def best_first(maze):
    # initialize start node
    start_node = Node(None, tuple(maze.spawn))
    # initialize end node
    end_node = Node(None, tuple(maze.end))

    #lists of nodes to visit and visited nodes
    yet_to_visit = []
    visited = []

     #Add start node
    yet_to_visit.append(start_node)

    #possible moves
    move = [[-1,0], #up
            [0,-1],  #left
            [1,0],  #down
            [0,1]]  #right

    #Loop until finds the goal
    while len(yet_to_visit) > 0:

        #Sort the list to get the node with the lowest cost first
        yet_to_visit.sort()

        #get current node
        current_node = yet_to_visit.pop(0)

        #Mark current node as visited
        visited.append(current_node)

        #If reached the goal, return the path solution
        if current_node == end_node:
            while current_node != start_node:
                maze.solution.append(current_node.position)
                current_node = current_node.parent

            return maze.solution

        
        for new_position in move:
            #Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            #Check if node position is out of boundaries
            if(node_position[0] > (len(maze.board) - 1) or
                node_position[0] < 0 or
                node_position[1] > (len(maze.board[0]) - 1) or
                node_position[1] < 0):         
                continue
            
            # check if node position is actually a wall
            if maze.board[node_position[0]][node_position[1]] == "-":   
                continue
            
            #Create neighbor node and checks if is in the visited list
            neighbor = Node(current_node, node_position)
            if neighbor in visited:
                continue
            
            #Create f value according to heuristic
            neighbor.f = heuristic(neighbor, end_node)

            #Check if neighbor is in yet_to_visit list and if it has a lower f value,
            # if not, add to yet_to_visit list
            if len([i for i in yet_to_visit if neighbor == i and neighbor.f >= i.f]) <= 0:
                yet_to_visit.append(neighbor)

    # return None if path is not found
    return None

#A star search        
def a_star(maze):
    # initialize start node
    start_node = Node(None, tuple(maze.spawn))
    # initialize end node
    end_node = Node(None, tuple(maze.end))

    #lists of nodes to visit and visited nodes
    yet_to_visit = []
    visited = []

    #Add start node
    yet_to_visit.append(start_node)
    
    #possible moves
    move = [[-1,0], #up
            [0,-1],  #left
            [1,0],  #down
            [0,1]]  #right

    #Loop until finds the goal
    while len(yet_to_visit) > 0:

        #Sort the list to get the node with the lowest cost first
        yet_to_visit.sort()

        #get current node
        current_node = yet_to_visit.pop(0)

        #Mark current node as visited
        visited.append(current_node)

        #If reached the goal, return the path solution
        if current_node == end_node:
            while current_node != start_node:
                maze.solution.append(current_node.position)
                current_node = current_node.parent

            return maze.solution

        
        for new_position in move:
            #Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            #Check if node position is out of boundaries
            if(node_position[0] > (len(maze.board) - 1) or
                node_position[0] < 0 or
                node_position[1] > (len(maze.board[0]) - 1) or
                node_position[1] < 0):         
                continue
            
            # check if node position is actually a wall
            if maze.board[node_position[0]][node_position[1]] == "-":   
                continue
            
            #Create neighbor node and checks if is in the visited list
            neighbor = Node(current_node, node_position)
            if neighbor in visited:
                continue
            
            #Create f,g and h values
            neighbor.g = current_node.g + maze.cost
            neighbor.h = heuristic(neighbor, end_node)
            neighbor.f = neighbor.g + neighbor.h

            #Check if neighbor is in yet_to_visit list and if it has a lower f value,
            # if not, add to yet_to_visit list
            if len([i for i in yet_to_visit if neighbor == i and neighbor.f >= i.f]) <= 0:
                yet_to_visit.append(neighbor)

    # return None if path is not found
    return None
       
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
        
# maze.print()

# bfs(maze)
# dfs(maze)start_time = time.time()
start_time = time.time()
best_first(maze)
print("Best-First Search:")
print(maze.solution[::-1])
print("--- %s seconds ---" % (time.time() - start_time))
start_time = time.time()
a_star(maze)
print("A star:")
print(maze.solution[::-1])
print("--- %s seconds ---" % (time.time() - start_time))

# hill_climbing(maze)