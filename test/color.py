import pygame

color_choices = [(10, 31, 142), (255, 215, 0), (0, 139, 0), (255, 255, 255),
              (208, 32, 144), (238, 130, 238), (0, 134, 139), (0, 197, 205),
              (109, 0, 0), (225, 0, 0), (129, 61, 28), (205, 104, 57),
              (75, 16, 129), (135, 48, 215), (42, 63, 174), (0, 205, 102)]

pygame.init()

WIDTH = 1920
HEIGHT = 1080
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Игрулька для мамульки')
font = pygame.font.Font(None, 62)
font2 = pygame.font.Font(None, 400)
fps = 30
timer = pygame.time.Clock()


run = True
while run:
    screen.fill('black')
    timer.tick(fps)

    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    pygame.draw.rect(screen, color_choices[tube_cols[i][j]], [x, 450 - (85 * j), 105, 85])


    pygame.display.flip()
pygame.quit()