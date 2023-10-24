import pygame
import numpy as np

all_colors = [(10, 31, 142), (255, 215, 0), (0, 139, 0), (255, 255, 255),
                (178, 2, 114), (238, 130, 238), (0, 114, 119), (0, 197, 205),
                (109, 0, 0), (225, 0, 0), (109, 41, 8), (205, 104, 57),
                (75, 16, 129), (135, 48, 215), (42, 63, 174), (0, 205, 102)]
AC_index = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]


test = [[0, 0], [1, 1, 1, 1], [2, 2, 2, 2], [3, 3, 3, 3], [4, 4, 4, 4], [0, 0], []]

pygame.init()

WIDTH = 1920
HEIGHT = 1080
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Игрулька для мамульки')
font = pygame.font.Font(None, 62)
font2 = pygame.font.Font(None, 400)
fps = 30
timer = pygame.time.Clock()

def color_level_choise():
    for i in range(10):
        x = random.randint(10, 15)
        print(x)
    pass
    
        
tubes_number = 10
level_colors = []
for i in range(tubes_number - 2):
    #print (level_colors[i])
    color = random.choice(AC_index)
    print (random.choice(AC_index))
    level_colors.append(color)
    AC_index.remove(color)
print (level_colors)
kolb_cveta = []
for index, level_colors in enumerate(level_colors):
    kolb_cveta.append([])
    print (level_colors, index)
    for j in range(4):
        kolb_cveta[index].append(level_colors)
print (type(kolb_cveta), kolb_cveta)


def generate_start():
    AC_index = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    tubes_number = 10
    tubes_colors = []
    level_colors = []
    kolb_cveta = []
    
    for i in range(tubes_number - 2):
        color = random.choice(AC_index)
        level_colors.append(color)
        AC_index.remove(color)
    
    for index, level_colors in enumerate(level_colors):
        kolb_cveta.append([])
        for j in range(4):
            kolb_cveta[index].append(level_colors)
    print (kolb_cveta)
    for i in range(tubes_number - 2):
        tubes_colors.append([])
        for j in range(4):
            color = random.choice(kolb_cveta,)
            tubes_colors[i].append(color)
            kolb_cveta.remove(color)
    
    return tubes_colors

print(generate_start())