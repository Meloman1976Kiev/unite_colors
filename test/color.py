import pygame
from numpy import random

color_choices = [(10, 31, 142), (255, 215, 0), (0, 139, 0), (255, 255, 255),
              (178, 2, 114), (238, 130, 238), (0, 114, 119), (0, 197, 205),
              (109, 0, 0), (225, 0, 0), (109, 41, 8), (205, 104, 57),
              (75, 16, 129), (135, 48, 215), (42, 63, 174), (0, 205, 102)]


test = [[0, 0, 0, 0], [1, 1, 1, 1], [2, 2, 2, 2], [3, 3, 3, 3], [4, 4, 4, 4]]

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
    
"""
run = True
while run:
    screen.fill('black')
    timer.tick(fps)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for x, number in enumerate(range (80, 2000, 120)):
        print (number, x)
        pygame.draw.rect(screen, color_choices[x], [number, 100, 80, 130])


    pygame.display.flip()
pygame.quit()
"""


tubes_number = random.randint(min, max)
    tubes_colors = []
    available_colors = []
    for i in range(tubes_number):
        tubes_colors.append([])
        if i < tubes_number - 2:
            for j in range(4):
                available_colors.append(i)
    for i in range(tubes_number - 2):
        for j in range(4):
            color = random.choice(available_colors)
            tubes_colors[i].append(color)
            available_colors.remove(color)