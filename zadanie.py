import copy
import random
import pygame

# initialize pygame
pygame.init()

# initialize game variables
WIDTH = 1920
HEIGHT = 1080
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Игрулька для мамульки')
font = pygame.font.Font(None, 62)
font2 = pygame.font.Font(None, 400)
fps = 30
timer = pygame.time.Clock()
color_choices = [(10, 31, 142), (255, 215, 0), (0, 139, 0), (255, 255, 255),
              (208, 32, 144), (238, 130, 238), (0, 134, 139), (0, 197, 205),
              (109, 0, 0), (225, 0, 0), (129, 61, 28), (205, 104, 57),
              (75, 16, 129), (135, 48, 215), (42, 63, 174), (0, 205, 102)]
tube_colors = []
initial_colors = []
# 10 - 14 tubes, always start with two empty
#tubes = 10
new_game = True
selected = False
dop_prob = False
tube_rects = []
select_rect = 100
win = False
level = 0



def new_level (level):
    if 0 <= level <= 20:
        random_min = 5
        random_max = 7
        parts = 4
    elif 21 <= level <= 40:
        random_min = 6
        random_max = 9
        parts = 4
    elif 41 <= level <= 60:
        random_min = 6
        random_max = 12
    elif 61 <= level <= 80:
        random_min = 6
        random_max = 16
    elif level > 80:
        random_min = 6
        random_max = 18
    return random_min, random_max


# select a number of tubes and pick random colors upon new game setup
def generate_start(level):
    min, max = new_level(level)
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
    print(tubes_colors)
    print(tubes_number)
    return tubes_colors


def get_offsets(prob_line):
    offset = (1920 - (prob_line * 105)) // (prob_line + 1)
    offset_with_prob = offset + 105
    return offset, offset_with_prob


def draw_rect_alpha(surface, color, rect):
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
    surface.blit(shape_surf, rect)



# draw all tubes and colors on screen, as well as indicating what tube was selected
def draw_tubes (tube_cols):
    tube_boxes = []
    tubes_num = len(tube_cols)
    if tubes_num % 2 == 0:
        tubes_per_row = tubes_num // 2
        chetnoe = True
    else:
        tubes_per_row = tubes_num // 2 + 1
        chetnoe = False
    
    spacing_1 = int((WIDTH - (tubes_per_row * 105)) // (tubes_per_row + 1))
    spacing_1_tube = spacing_1 + 105
    #print (tube_colors)
    for i in range(tubes_per_row):
        for j in range(len(tube_cols[i])):
            if j == 0:
                pygame.draw.polygon(screen, color_choices[tube_cols[i][j]], ([spacing_1, 450], [spacing_1, 510], [spacing_1 + 25, 535], 
                                    [spacing_1 + 79, 535], [spacing_1 + 104, 510], [spacing_1 + 104, 450]))
            else:
                pygame.draw.rect(screen, color_choices[tube_cols[i][j]], [spacing_1, 450 - (85 * j), 105, 85])
        box = pygame.draw.polygon(screen, (179, 204, 255), 
                                    [[spacing_1, 170], [spacing_1, 510], [spacing_1 + 25, 535], 
                                    [spacing_1 + 79, 535], [spacing_1 + 104, 510], [spacing_1 + 104, 170]], 3)
        if select_rect == i:
            pygame.draw.rect(screen, 'green', [spacing_1 - 20, 145, 145, 415], 10, 10)
        tube_boxes.append(box)
        spacing_1 += spacing_1_tube
        
    
    if chetnoe:
        spacing_2 = int((WIDTH - (tubes_per_row * 105)) // (tubes_per_row + 1))
        spacing_2_tube = spacing_2 + 105
        for i in range(tubes_per_row):
            for j in range(len(tube_cols[i + tubes_per_row])):
                if j == 0:
                    pygame.draw.polygon(screen, color_choices[tube_cols[i + tubes_per_row][j]], 
                                        ([spacing_2, 900], [spacing_2, 960], [spacing_2 + 25, 985], 
                                    [spacing_2 + 79, 985], [spacing_2 + 104, 960], [spacing_2 + 104, 900]))
                else:
                    pygame.draw.rect(screen, color_choices[tube_cols[i + tubes_per_row][j]], 
                                    [spacing_2, 900 - (85 * j), 105, 85], 0, 3)
                                    
            box = pygame.draw.polygon(screen, (179, 204, 255), 
                                    [[spacing_2, 620], [spacing_2, 960], [spacing_2 + 25, 985], 
                                    [spacing_2 + 79, 985], [spacing_2 + 104, 960], [spacing_2 + 104, 620]], 3)
            if select_rect == i + tubes_per_row:
                pygame.draw.rect(screen, 'green', [spacing_2 - 20, 595, 145, 415], 10, 10)
            tube_boxes.append(box)
            spacing_2 += spacing_2_tube

    else:
        spacing_2 = int((WIDTH - ((tubes_per_row - 1) * 105)) // tubes_per_row)
        spacing_2_tube = spacing_2 + 105
        
        for i in range(tubes_per_row - 1):
            for j in range(len(tube_cols[i + tubes_per_row])):
                if j == 0:
                    pygame.draw.polygon(screen, color_choices[tube_cols[i + tubes_per_row][j]], 
                                        ([spacing_2, 900], [spacing_2, 960], [spacing_2 + 25, 985], 
                                    [spacing_2 + 79, 985], [spacing_2 + 104, 960], [spacing_2 + 104, 900]))
                else:
                    pygame.draw.rect(screen, color_choices[tube_cols[i + tubes_per_row][j]], 
                                    [spacing_2, 900 - (85 * j), 105, 85], 0, 3)
            box = pygame.draw.polygon(screen, (179, 204, 255), 
                                    [[spacing_2, 620], [spacing_2, 960], [spacing_2 + 25, 985], 
                                    [spacing_2 + 79, 985], [spacing_2 + 104, 960], [spacing_2 + 104, 620]], 3)
            if select_rect == i + tubes_per_row:
                pygame.draw.rect(screen, 'green', [spacing_2 - 20, 595, 145, 415], 10, 10)
            tube_boxes.append(box)
            spacing_2 += spacing_2_tube
    return tube_boxes


# determine the top color of the selected tube and destination tube,
# as well as how long a chain of that color to move
def calc_move(colors, selected_rect, destination):
    color_on_top = 100
    color_to_move = 100
    chain = True
    length = 1
    if len(colors[selected_rect]) > 0:
        color_to_move = colors[selected_rect][-1]
        for i in range(1, len(colors[selected_rect])):
            if chain:
                if colors[selected_rect][-1 - i] == color_to_move:
                    length += 1
                else:
                    chain = False
    if 4 > len(colors[destination]):
        if len(colors[destination]) == 0:
            color_on_top = color_to_move
        else:
            color_on_top = colors[destination][-1]
    if color_on_top == color_to_move:
        for i in range(length):
            if len(colors[destination]) < 4:
                if len(colors[selected_rect]) > 0:
                    colors[destination].append(color_on_top)
                    colors[selected_rect].pop(-1)
    #print(colors, length)
    return colors


# check if every tube with colors is 4 long and all the same color. That's how we win
def check_victory(colors):
    won = True
    for i in range(len(colors)):
        if len(colors[i]) > 0:
            if len(colors[i]) != 4:
                won = False
            else:
                main_color = colors[i][-1]
                for j in range(len(colors[i])):
                    if colors[i][j] != main_color:
                        won = False
    return won

#my version of check winning
def check_win (list_tub):
    tube_true_false = []
    for t in list_tub:
        tube_true_false.append(all(i == t[0] for i in t))
    return all(i == True for i in tube_true_false)


def same_color (tube):
    T_F_color = all(i == tube[0] for i in tube)
    return T_F_color



# main game loop
run = True
while run:
    screen.fill('black')
    timer.tick(fps)
    # generate game board on new game, make a copy of the colors in case of restart
    if new_game:
        tube_colors = generate_start(level)
        initial_colors = copy.deepcopy(tube_colors)
        new_game = False
        level += 1
    # draw tubes every cycle
    else:
        tube_rects = draw_tubes(tube_colors)
    # check for victory every cycle
    win = check_victory(tube_colors)
    #win = check_win (tube_colors)
    # event handling - Quit button exits, clicks select tubes, enter and space for restart and new board
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                tube_colors = copy.deepcopy(initial_colors)
            elif event.key == pygame.K_RETURN:
                new_game = True
            elif event.key == pygame.K_BACKSPACE:
                nazad = 1
            elif event.key == pygame.K_d:
                tube_colors.append([])
            elif event.key == pygame.K_r:
                tube_colors.pop(-1)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not selected:
                for item in range(len(tube_rects)):
                    if tube_rects[item].collidepoint(event.pos):
                        if len (tube_colors[item]) == 4 and same_color(tube_colors[item]) == True:
                            selected = False
                            select_rect = 100
                        else:
                            selected = True
                            select_rect = item

            else:
                for item in range(len(tube_rects)):
                    if tube_rects[item].collidepoint(event.pos):
                        dest_rect = item
                        tube_colors = calc_move(tube_colors, select_rect, dest_rect)
                        selected = False
                        select_rect = 100
    # draw 'victory' text when winning in middle, always show restart and new board text at top
    if win:
        win_text = font2.render('ПОБЕДА!', True, 'white')
        screen.blit(win_text, win_text.get_rect(center=(WIDTH/2 + 4, 574)))
        win_text = font2.render('ПОБЕДА!', True, (200, 0, 0))
        screen.blit(win_text, win_text.get_rect(center=(WIDTH/2, 570)))
        

        #video = ПЛОХО! виснет
        #pygame.display.set_caption('Victory!')
        #clip = VideoFileClip('/home/m/fire.mp4')
        #clip.preview()
        #new_game = True
    
    up_text = font.render("Уровень", True, 'white')
    place = (WIDTH/2 - 150, 50)
    screen.blit(up_text, place)
    up_text_2 = font.render(str(level), True, 'white')
    place = (WIDTH/2 + 50, 50)
    screen.blit(up_text_2, place)


    #screen.blit(restart_text, (10, 10))

    # display all drawn items on screen, exit pygame if run == False
    pygame.display.flip()
pygame.quit()