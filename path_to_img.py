# Grupo:
#  Nome: Abner Eduardo Silveira Santos  NUSP: 10692012
#  Nome: Gyovana Mayara Moriyama        NUSP: 10734387
#  Nome: Henrique Matarazo Camillo      NUSP: 10294943
#  Nome: João Pedro Uchôa Cavalcante    NUSP: 10801169

import sys
import imageio
import numpy as np

# Transforms the input from the file into a matrix
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

# Converts each character into a color
def img_converter(maze):

    img = np.zeros((len(maze), len(maze[0]), 3))

    color = {
        '*': [255, 214, 191],   # Empty space
        '-': [48, 18, 45],      # Wall
        'x': [63, 127, 191],    # Explored space
        'O': [203, 45, 62],     # Chosen path
        '#': [77, 8, 42],       # Entrance
        '$': [239, 71, 58]      # Exit
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