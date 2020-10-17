import time
import copy


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
                solution = bfs_traceback(maze, parents)
                original_maze.solution.append(solution)
                maze.print()
                return solution
            # If hasn't reached the end yet, marks the node as visited and add it to the queue
            else:
                maze.board[move[0]][move[1]] = 'x'
                queue.append(move)

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

def dfs(maze):
    return

def best_first(maze):
    return

def hill_climbing(maze):
    return

def a_star(maze):
    return

class Maze:
    def __init__(self, x, y):
        self.shape = (x, y)
        self.board = [[None for _ in range(y)] for _ in range(x)]
        self.spawn = ()
        self.end = ()
        self.solution = []

    def print(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                print(self.board[i][j], end=' ')
            print()

#===================================#

possible_moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]

shape = input().split()
x = int(shape[0])
y = int(shape[1])

maze = Maze(x, y)

for i in range(x):
    line = [char for char in input()]
    for j in range(len(line)):
        if (line[j] == '#'):
            maze.spawn = i, j
        elif (line[j] == '$'):
            maze.end = i, j

        maze.board[i][j] = line[j] 
        
bfs(maze)
dfs(maze)
best_first(maze)
a_star(maze)
hill_climbing(maze) 