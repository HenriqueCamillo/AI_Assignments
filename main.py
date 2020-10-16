import time

def bfs(maze):
    return

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
        self.board = [[None for _ in range(y)] for _ in range(x)]
        self.spawn = []
        self.end = []
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
    line = [char for char in input()]
    for j in range(len(line)):
        if (j == "$"):
            maze.spawn = i, j
        elif (j == "#"):
            maze.end = i, j

        maze.board[i][j] = line[j] 
        
maze.print()

bfs(maze)
dfs(maze)
best_first(maze)
a_star(maze)
hill_climbing(maze)