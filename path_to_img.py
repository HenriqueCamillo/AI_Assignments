import sys
import imageio
import numpy as np

def file_load(filename):
    
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

def img_converter(maze):

    img = np.zeros((len(maze), len(maze[0]), 3))

    color = {
        '*': [255, 214, 191],
        '-': [48, 18, 45],
        'x': [135, 7, 52],
        'o': [203, 45, 62],
        '#': [77, 8, 42],
        '$': [239, 71, 58]
    }

    for x in range(0, img.shape[0]):
        for y in range(0, img.shape[1]):
            img[x][y] = color.get(maze[x][y])

    return img

# Loads string
maze = file_load(sys.argv[1])

# Transforms it into an image
img = img_converter(maze)

# Writes image
imageio.imwrite(sys.argv[2], img.astype(np.uint8))