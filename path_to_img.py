import sys
import imageio
import numpy as np

def load_maze(filename):
    
    try:
        with open(filename, 'r') as text_file:
            maze_text = text_file.read()
    except:
        print('We could not open the file you requested.')
        exit(1)

    lines = maze_text.splitlines()

    shape = lines[0].split()
    x = int(shape[0])
    y = int(shape[1])
    maze = [[None for i in range(y)] for j in range(x)] 

    for i in range(x):
        line = [char for char in lines[i+1] if char != '\r']
        for j in range(len(line)):
            maze[i][j] = line[j]

    return maze

def str_to_img(maze):

    img = np.zeros((len(maze), len(maze[0]), 3))

    for x in range(0, img.shape[0]):
        for y in range(0, img.shape[1]):
        
            # Empty space
            if maze[x][y] == '*':
                img[x][y] = [255, 214, 191]

            # Obstacle
            elif maze[x][y] == '-':
                img[x][y] = [48, 18, 45]

            # Analyzed paths
            elif maze[x][y] == 'x':
                img[x][y] = [135, 7, 52]

            # Found path
            elif maze[x][y] == 'o':
                img[x][y] = [203, 45, 62]

            # Spawn
            elif maze[x][y] == '#':
                img[x][y] = [77, 8, 42]

            # End
            elif maze[x][y] == '$':
                img[x][y] = [239, 71, 58]

    return img

# Loads string
maze = load_maze(sys.argv[1])

# Transforms it into an image
img = str_to_img(maze)

# Writes image
imageio.imwrite(sys.argv[2], img.astype(np.uint8))