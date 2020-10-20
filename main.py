import time
import copy
import random


# Returns a list of all valid moves based on the possible_moves and a position in a maze
def get_valid_moves(board, pos):
    moves = []

    for move in possible_moves:
        new_pos = (pos[0] + move[0], pos[1] + move[1])

        # If out of bounds, skip
        if new_pos[0] < 0 or new_pos[0] >= maze.shape[0] or new_pos[1] < 0 or new_pos[1] >= maze.shape[1]: 
            continue

        # If an empty space, or the solution, adds position to move list
        if board[new_pos[0]][new_pos[1]] == '*' or board[new_pos[0]][new_pos[1]] == '$':
            moves.append(new_pos)

    return moves

def restore_spawn_and_end(maze):
    maze.board[maze.spawn[0]][maze.spawn[1]] = '#'
    maze.board[maze.end[0]][maze.end[1]] = '$'

# Finds maze solution using Breadth First Search algorithm
# Returns the solution, or None, if the maze doesn't have any
def bfs(original_maze):

    # Creates a copy of the original maze
    maze = copy.deepcopy(original_maze)
    queue = [maze.spawn]    # BFS queue, starting on maze spawn
    parents = {}            # Stores the parent of each node, so that we can find the path

    # Keeps running while there are nodes in the queue
    while queue:
        # Gets all valid moves of the next node of the queue
        pos = queue.pop(0)
        moves = get_valid_moves(maze.board, pos)

        # For each of them, saves its parent and checks if has reached the end of the maze
        for move in moves:
            parents[move] = pos

            # If has reached the end, discovers tracback and returns
            if move == maze.end:
                original_maze.bfs_solution = bfs_traceback(maze, parents)

                # prints result
                restore_spawn_and_end(maze)
                maze.print('bfs.txt')

                return original_maze.bfs_solution
            # If hasn't reached the end yet, marks the node as visited and add it to the queue
            else:
                maze.board[move[0]][move[1]] = 'x'
                queue.append(move)

    # prints result
    restore_spawn_and_end(maze)
    maze.print('bfs.txt')
    return None

# Finds the path of the solution after it was found and the parent of each node was set
# Marks path nodes with a 'O' and returns a list of tuples representing the path
def bfs_traceback(maze, parents):
    path = [maze.end]
    while path[0] != maze.spawn:
        parent = parents[path[0]]
        maze.board[parent[0]][parent[1]] = 'O'
        path.insert(0, parent)
    return path

# Fills te previous_access_matrix while doing the actual DFS
def aux_dfs(maze, current_node, path):
    if current_node == maze.end:
        path.append(current_node)
        return True

    # Marks the current node that it is in as already visited
    maze.board[current_node[0]][current_node[1]] = 'x'

    # Each cell bellow puts the current node on the node that will be acessed when the function calls it
    # The conditions are that it does not goes out of the matrix and is a valid walk point

    # Walks to the right if the conditions to do so are met
    if(current_node[1]+1 < maze.shape[1] and (maze.board[current_node[0]][current_node[1]+1] == '*' or maze.board[current_node[0]][current_node[1]+1] == '$')):
        if aux_dfs(maze, (current_node[0], current_node[1]+1), path):
            maze.board[current_node[0]][current_node[1]] = 'O'
            path.append(current_node)
            return True
  
  # Walks to the bottom if the conditions to do so are met
    if(current_node[0]+1 < maze.shape[0] and (maze.board[current_node[0]+1][current_node[1]] == '*' or maze.board[current_node[0]+1][current_node[1]] == '$')):
        if aux_dfs(maze, (current_node[0]+1, current_node[1]), path):
            maze.board[current_node[0]][current_node[1]] = 'O'
            path.append(current_node)
            return True

    # Walks to the left if the conditions to do so are met
    if(current_node[1]-1 > 0 and (maze.board[current_node[0]][current_node[1]-1] == '*' or maze.board[current_node[0]][current_node[1]-1] == '$')):
        if aux_dfs(maze, (current_node[0], current_node[1]-1), path):
            maze.board[current_node[0]][current_node[1]] = 'O'
            path.append(current_node)
            return True

    # Walks to the top if the conditions to do so are met
    if(current_node[0]-1 > 0 and (maze.board[current_node[0]-1][current_node[1]] == '*' or maze.board[current_node[0]-1][current_node[1]] == '$')):
        if aux_dfs(maze, (current_node[0]-1, current_node[1]), path):
            maze.board[current_node[0]][current_node[1]] = 'O'
            path.append(current_node)
            return True

    return False

# Finds the path while recovering an matrix that has in each of the nodes the previous node from wich the current was accessed
# that was generated while doin the DFS
def dfs(original_maze):
    # Creates a copy of the original maze
    maze = copy.deepcopy(original_maze)

    # Creates an auxiliar matrix that stores the node from where the current node was accessed from
    previous_access_matrix = [[None for _ in range(y)] for _ in range(x)]

    # Fills te previous_access_matrix while doing the actual DFS
    path = []
    aux_dfs(maze, maze.spawn, path)

    # Recover the inverted path from the previous_access_matrix
    # path = dfs_recover_inverted_path(previous_access_matrix, maze.spawn, maze.end)

    # Inverts the inverted path, correcting it
    path = path[::-1]
    original_maze.dfs_solution = path

    restore_spawn_and_end(maze)
    maze.print('dfs.txt')

    return path if len(path) > 0 else None

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
def best_first(original_maze):
    maze = copy.deepcopy(original_maze)

    # initialize start node
    start_node = Node(None, tuple(maze.spawn))
    # initialize end node
    end_node = Node(None, tuple(maze.end))

    #lists of nodes to visit and visited nodes
    yet_to_visit = [start_node]
    visited = []

    #Loop until finds the goal
    while len(yet_to_visit) > 0:

        #Sort the list to get the node with the lowest cost first
        yet_to_visit.sort()

        #get current node
        current_node = yet_to_visit.pop(0)

        #Mark current node as visited
        visited.append(current_node)
        maze.board[current_node.position[0]][current_node.position[1]] = 'x'

        #If reached the goal, return the path solution
        if current_node == end_node:
            while current_node != start_node:
                original_maze.best_first_solution.insert(0, current_node.position)
                current_node = current_node.parent
            original_maze.best_first_solution.insert(0, current_node.position)
            
            # prints result
            restore_spawn_and_end(maze)
            maze.print('best_first.txt')

            return maze.best_first_solution

        moves = get_valid_moves(maze.board,current_node.position)
        
        for move in moves:
            
            #Create neighbor node and checks if is in the visited list
            neighbor = Node(current_node, move)
            if neighbor in visited:
                continue
            
            #Create f value according to heuristic
            neighbor.f = heuristic(neighbor, end_node)

            #Check if neighbor is in yet_to_visit list and if it has a lower f value,
            # if not, add to yet_to_visit list
            if len([i for i in yet_to_visit if neighbor == i and neighbor.f >= i.f]) <= 0:
                yet_to_visit.append(neighbor)

    restore_spawn_and_end(maze)
    maze.print('best_first.txt')

    # return None if path is not found
    return None

#A star search        
def a_star(original_maze):
    maze = copy.deepcopy(original_maze)

    # initialize start node
    start_node = Node(None, tuple(maze.spawn))
    # initialize end node
    end_node = Node(None, tuple(maze.end))

    #lists of nodes to visit and visited nodes
    yet_to_visit = [start_node]
    visited = []
    
    #Loop until finds the goal
    while len(yet_to_visit) > 0:

        #Sort the list to get the node with the lowest cost first
        yet_to_visit.sort()

        #get current node
        current_node = yet_to_visit.pop(0)

        #Mark current node as visited
        visited.append(current_node)
        maze.board[current_node.position[0]][current_node.position[1]] = 'x'

        #If reached the goal, return the path solution
        if current_node == end_node:
            while current_node != start_node:
                original_maze.a_star_solution.insert(0, current_node.position)
                current_node = current_node.parent
            original_maze.a_star_solution.insert(0, current_node.position)

            # prints result
            restore_spawn_and_end(maze)
            maze.print('a_start.txt')

            return original_maze.a_star_solution

        moves = get_valid_moves(maze.board, current_node.position)
        
        for move in moves:
           
            #Create neighbor node and checks if is in the visited list
            neighbor = Node(current_node, move)
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

    # prints result
    restore_spawn_and_end(maze)
    maze.print('a_star.txt')

    # return None if path is not found
    return None

#Manhattan distance used in hill climbing heuristic
def hc_heuristic(current, end):
    return ((abs(current[0] - end[0])) + (abs(current[1] - end[1])))

def hill_climbing(original_maze):
    # Creates a copy of the original maze
    maze = copy.deepcopy(original_maze)

    # Sets initial position
    cur_pos = maze.spawn
    prev_pos = None

    # Get valid moves for that position
    moves = get_valid_moves(maze.board, cur_pos)

    # While there are valid moves
    while moves:
        # If our hill climber has moved, add to solution
        if cur_pos != prev_pos:
            original_maze.hill_climbing_solution.append(cur_pos)

        # Stochastic hill climbing
        # We figured this would be the best for a simple maze because no direction is always better than another for any maze
        # so where we start doesn't matter. And since we only have 4 neighbors, you can only get 1 unit closer at a time, so
        # a steepest-ascent hill climb would only make it slower
        move = random.choice(moves)

        # Stop movement if we reach the end
        if move == maze.end:
            original_maze.hill_climbing_solution.append(move)
            
            # Prints result
            restore_spawn_and_end(maze)
            maze.print('hill_climbing.txt')

            return original_maze.hill_climbing_solution
        else:
            prev_pos = cur_pos

            # If moving to the selected pos would make the climber get closer to the end, move
            if hc_heuristic(move, maze.end) <= hc_heuristic(cur_pos, maze.end):
                cur_pos = move

            # So that we don't evaluate it again
            maze.board[move[0]][move[1]] = 'x'

            # Get new valid moves
            moves = get_valid_moves(maze.board, cur_pos)

    # Prints result
    restore_spawn_and_end(maze)
    maze.print('hill_climbing.txt')
    # If we can't reach the end
    return None
       
class Maze:
    def __init__(self, x, y):
        self.shape = (x, y)
        self.board = [[None for _ in range(y)] for _ in range(x)]
        self.spawn = ()
        self.end = ()
        self.bfs_solution = []
        self.dfs_solution = []
        self.best_first_solution = []
        self.a_star_solution = []
        self.hill_climbing_solution = []
        self.cost = 1

    def print(self, filename):
        file = open(filename, 'w')
        file.write(str(self.shape[0]) + ' ' + str(self.shape[1]) + '\n')
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                print(self.board[i][j], end=' ')
                file.write(str(self.board[i][j]) + ' ')
            print()
            file.write('\n')
        file.close()


#===================================#

possible_moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]

shape = input().split()
x = int(shape[0])
y = int(shape[1])

maze = Maze(x, y)

for i in range(x):
    line = [char for char in input() if char != '\r']
    for j in range(len(line)):
        if (line[j] == '#'):
            maze.spawn = i, j
        elif (line[j] == '$'):
            maze.end = i, j
        maze.board[i][j] = line[j]


print("BFS Search:")
start_time = time.time()
solution = bfs(maze)

print(maze.bfs_solution)
print("--- %s seconds ---" % (time.time() - start_time))
if solution == None:
    print("Has not found any solution")
    

print("\nDFS Search:")
start_time = time.time()
solution = dfs(maze)

print(maze.dfs_solution)
print("--- %s seconds ---" % (time.time() - start_time))
if solution == None:
    print("Has not found any solution")

print("\nBest-First Search:")
start_time = time.time()
solution = best_first(maze)

print(maze.best_first_solution)
print("--- %s seconds ---" % (time.time() - start_time))
if solution == None:
    print("Has not found any solution")

print("\nA star:")
start_time = time.time()
solution = a_star(maze)

print(maze.a_star_solution)
print("--- %s seconds ---" % (time.time() - start_time))
if solution == None:
    print("Has not found any solution")

print("\nHill Climbing:")
start_time = time.time()
solution = hill_climbing(maze)

print(maze.hill_climbing_solution)
print("--- %s seconds ---" % (time.time() - start_time))
if solution == None:
    print("Has not found any solution")