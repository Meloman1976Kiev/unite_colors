import numpy as np
import pygame


# initialize pygame
pygame.init()

# initialize game variables
WIDTH = 1920
HEIGHT = 1080
#screen = pygame.display.set_mode([WIDTH, HEIGHT])
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

pygame.display.set_caption('Игрулька для мамульки')
font = pygame.font.Font(None, 62)
font2 = pygame.font.Font(None, 400)
font3 = pygame.font.Font(None, 58)

timer = pygame.time.Clock()
# set FPS, in my case FPS = 30
timer.tick(30)

# игровые цвета
all_colors = [(10, 31, 142), (255, 215, 0), (0, 139, 0), (255, 255, 255),
              (208, 32, 144), (238, 130, 238), (0, 134, 139), (0, 197, 205),
              (109, 0, 0), (225, 0, 0), (129, 61, 28), (205, 104, 57),
              (75, 16, 129), (135, 48, 215), (42, 63, 174), (0, 205, 102)]

# задает мин и макс число колб для игры в зависимости от номера уровня
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

# определяет какие цвета участвуют в игре, создает случайную подборку
def generate_start(level):
    AC_index = [i for i in range(16)]
    min, max = new_level(level)
    tubes_number = np.random.randint(min, max)
    tubes_colors = []
    level_colors = []
    kolb_cveta = []
    clear = []

    for i in range(tubes_number - 2):
        color = np.random.choice(AC_index)
        level_colors.append(color)
        AC_index.remove(color)
    for i in level_colors:
        for j in range(4):
            kolb_cveta.append(i)
    arr = np.asarray(kolb_cveta)
    np.random.shuffle(arr)
    random_kolb_cveta = arr.tolist()
    for i in range(tubes_number - 2):
        clear.append([])
        for j in range(4):
            clear[i].append(random_kolb_cveta[0])
            del random_kolb_cveta[0]
            

    return clear

# создает колбы для игры так, чтобы не было подрях ТРЕХ одинаковых цветов
def no_3_same_parts(level):
    drob = False
    while not drob:
        tubes = generate_start(level)
        tub = sum(tubes, [])
        ser = 1
        for i in range(len(tub)-1):
            drob = True
            if tub[i] == tub[i+1]:
                ser += 1
                if ser == 3:
                    drob = False
                    break     
            else:
                ser = 1
                
    tubes.append([])
    tubes.append([])
    return tubes

# высчитывает отступы между пробирками в ряду
def get_offsets(prob_line):
    offset = (1920 - (prob_line * 105)) // (prob_line + 1)
    offset_with_prob = offset + 105
    return offset, offset_with_prob

# draw all tubes and colors on screen, as well as indicating what tube was selected
def draw_tubes (kolbs):
    tube_boxes = []
    
    #Чет/нечет и деление на две строки
    tubes_num = len(kolbs)
    if tubes_num % 2 == 0:
        tubes_per_row = tubes_num // 2
        chetnoe = True
    else:
        tubes_per_row = tubes_num // 2 + 1
        chetnoe = False
    
    #Отступы для рисования колб
    spacing_1 = int((WIDTH - (tubes_per_row * 105)) // (tubes_per_row + 1))
    spacing_1_tube = spacing_1 + 105
    
    #Рисование (tube_colors)
    for i in range(tubes_per_row):
        for j in range(len(kolbs[i])):
            if j == 0:
                pygame.draw.polygon(screen, all_colors[kolbs[i][j]], ([spacing_1, 500], [spacing_1, 560], [spacing_1 + 25, 585], 
                                    [spacing_1 + 79, 585], [spacing_1 + 104, 560], [spacing_1 + 104, 500]))
            else:
                pygame.draw.rect(screen, all_colors[kolbs[i][j]], [spacing_1, 500 - (85 * j), 105, 85])
        box = pygame.draw.polygon(screen, (179, 204, 255), 
                                    [[spacing_1, 220], [spacing_1, 560], [spacing_1 + 25, 585], 
                                    [spacing_1 + 79, 585], [spacing_1 + 104, 560], [spacing_1 + 104, 220]], 3)
        if select_rect == i:
            pygame.draw.rect(screen, (70, 70, 155), [spacing_1 - 30, 185, 165, 435], 15, 15)
        tube_boxes.append(box)
        spacing_1 += spacing_1_tube
        
    
    if chetnoe:
        spacing_2 = int((WIDTH - (tubes_per_row * 105)) // (tubes_per_row + 1))
        spacing_2_tube = spacing_2 + 105
        for i in range(tubes_per_row):
            for j in range(len(kolbs[i + tubes_per_row])):
                if j == 0:
                    pygame.draw.polygon(screen, all_colors[kolbs[i + tubes_per_row][j]], 
                                        ([spacing_2, 950], [spacing_2, 1010], [spacing_2 + 25, 1035], 
                                    [spacing_2 + 79, 1035], [spacing_2 + 104, 1010], [spacing_2 + 104, 950]))
                else:
                    pygame.draw.rect(screen, all_colors[kolbs[i + tubes_per_row][j]], 
                                    [spacing_2, 950 - (85 * j), 105, 85], 0, 3)
                                    
            box = pygame.draw.polygon(screen, (179, 204, 255), 
                                    [[spacing_2, 670], [spacing_2, 1010], [spacing_2 + 25, 1035], 
                                    [spacing_2 + 79, 1035], [spacing_2 + 104, 1010], [spacing_2 + 104, 670]], 3)
            if select_rect == i + tubes_per_row:
                pygame.draw.rect(screen, (70, 70, 155), [spacing_2 - 30, 635, 165, 435], 15, 15)
            tube_boxes.append(box)
            spacing_2 += spacing_2_tube

    else:
        spacing_2 = int((WIDTH - ((tubes_per_row - 1) * 105)) // tubes_per_row)
        spacing_2_tube = spacing_2 + 105
        
        for i in range(tubes_per_row - 1):
            for j in range(len(kolbs[i + tubes_per_row])):
                if j == 0:
                    pygame.draw.polygon(screen, all_colors[kolbs[i + tubes_per_row][j]], 
                                        ([spacing_2, 950], [spacing_2, 1010], [spacing_2 + 25, 1035], 
                                    [spacing_2 + 79, 1035], [spacing_2 + 104, 1010], [spacing_2 + 104, 950]))
                else:
                    pygame.draw.rect(screen, all_colors[kolbs[i + tubes_per_row][j]], 
                                    [spacing_2, 950 - (85 * j), 105, 85], 0, 3)
            box = pygame.draw.polygon(screen, (179, 204, 255), 
                                    [[spacing_2, 670], [spacing_2, 1010], [spacing_2 + 25, 1035], 
                                    [spacing_2 + 79, 1035], [spacing_2 + 104, 1010], [spacing_2 + 104, 670]], 3)
            if select_rect == i + tubes_per_row:
                pygame.draw.rect(screen, (70, 70, 155), [spacing_2 - 30, 635, 165, 435], 15, 15)
            tube_boxes.append(box)
            spacing_2 += spacing_2_tube
    return tube_boxes

# Проверка на возможность перемещения (и само перемещение) цвета из колбы в колбу
# Перед перемещением создаются копии (их число определяется nazad_step_max) на случай "Назад"
def prov_perem(a, b, nazad_step, nazad_step_max, nazad_list):

    kolb_1 = tube_colors[a]
    kolb_2 = tube_colors[b]
    if len(kolb_1) > 0 and len(kolb_2) < 4:
        #если колаба dest не пустая
        if len(kolb_2) > 0:
            if nazad_step_max > 0:
                if nazad_step < nazad_step_max:
                    nazad_list.append(copy_list(tube_colors))
                    nazad_step += 1
                else:
                    nazad_list.pop(0)
                    nazad_list.append(copy_list(tube_colors))
            while len (kolb_2) != 4 and len(kolb_1) > 0 and kolb_1[-1] == kolb_2[-1]:
                kolb_2.append(kolb_1[-1])
                kolb_1.pop(-1)

        #если колаба dest пустая
        else:
            if nazad_step_max > 0:
                if nazad_step < nazad_step_max:
                    nazad_list.append(copy_list(tube_colors))
                    nazad_step += 1
                else:
                    nazad_list.pop(0)
                    nazad_list.append(copy_list(tube_colors))
            kolb_2.append(kolb_1[-1])
            kolb_1.pop(-1)
            while len (kolb_2) != 4 and len(kolb_1) > 0 and kolb_1[-1] == kolb_2[-1]:
                kolb_2.append(kolb_1[-1])
                kolb_1.pop(-1)
            

    return nazad_step, nazad_list

# проверка на победу
def check_win (list_tub):
    tube_true_false = []
    for t in list_tub:
        if len(t) == 0 or len(t) == 4:
            tube_true_false.append(all(i == t[0] for i in t))
        else: 
            return False
    return all(i == True for i in tube_true_false)

# проверка, заполнена ли колба одним цветом (полная)
def same_color (tube):
    T_F_color = all(i == tube[0] for i in tube)
    return T_F_color

# копирование/клонирование/дипкопи списка без использования deepcopy
def copy_list (list):
    copy = []
    for i in list:
        copy.append(i[:])
    return copy

# выбирает из файла случайный факт. 
# возращает list и срез (разбитие на строки шириной до 62 символов) 
def fact_choice():
    text = open('facts.txt', 'r', encoding='windows-1251')
    
    #text_1 = 'Во Франции законом запрещено называть свиней именем Наполеон. Других животных запрет не касается.'
    #text_1 = 'На Северном полюсе теплее, чем на Южном. Северный полюс находится на уровне моря, а Южный – на высоте 2,8 км над уровнем моря. Кроме того, Северный полюс освещается Солнцем почти на наделю дольше, чем Южный.'
    
    random_line = []
    while len(random_line) == 0:
        random_line = np.random.choice(text.readlines())

    rl_list = random_line.split()
    #rl_list = text_1.split()
    #print (rl_list)
    srez = [0]
    symbols_in_str = len(rl_list[0])
    for i in range(1, len(rl_list)):
        if symbols_in_str + 1 + len(rl_list[i]) <= 62:
            symbols_in_str += 1
            symbols_in_str += len(rl_list[i])
                       
        else:
            srez.append(i)
            symbols_in_str = (len(rl_list[i]))
        
    return rl_list, srez

# рисует прямоугольник со срезанными углами с помощью polygon (8 точек)
def srez_polyg(srez, x_start, y_start, shir, vis, cvet):
    return pygame.draw.polygon(screen, cvet, [[x_start + srez, y_start], [x_start + shir - srez, y_start],
                                           [x_start + shir, y_start + srez], [x_start + shir, y_start + vis - srez],
                                           [x_start + shir - srez, y_start + vis], [x_start + srez, y_start + vis],
                                           [x_start, y_start + vis - srez], [x_start, y_start + srez]])

# Затемнение экрана после победы
def fade_out(shir, vis):
    fade = pygame.Surface((shir, vis))
    fade.fill('black')
    for alp in range(0, 1000, 5):
        fade.set_alpha(alp/10)
        screen.blit(fade, (0,0))
        pygame.display.update()

# Верхняя строка с очками, уровнем и тд, возращает 7 боксов для клика
def up_line():
    menu_box = srez_polyg (15, 60, 35, 120, 100, 'gray55')
    menu_image = pygame.image.load("images/set_new.png").convert_alpha()
    menu_image2 = pygame.transform.scale_by(menu_image, 1.4)
    menu_image2_rect = menu_image2.get_rect()
    menu_image2_rect.center = menu_box.center
    screen.blit(menu_image2, menu_image2_rect)
    
    restart_box = srez_polyg (15, 240, 35, 120, 100, 'slateblue1')
    restart_image = pygame.image.load("images/restart_new.png").convert_alpha()
    restart_image2 = pygame.transform.scale_by(restart_image, 1.3)
    restart_image2_rect = restart_image2.get_rect()
    restart_image2_rect.center = restart_box.center
    screen.blit(restart_image2, restart_image2_rect)    
    
    points_box = srez_polyg (15, 420, 35, 260, 100, 'gold')
    points_string = str(points)
    points_text = pygame.font.Font(None, 120).render(points_string, True, 'black')
    points_text_rect = points_text.get_rect()
    points_text_rect.center = points_box.center
    screen.blit(points_text, points_text_rect)
    
    level_box = srez_polyg (15, 740, 35, 400, 100, 'dark green')
    level_string = 'Уровень ' + str(level)
    level_text = pygame.font.Font(None, 70).render(level_string, True, 'white')
    level_text_rect = level_text.get_rect()
    level_text_rect.center = level_box.center
    screen.blit(level_text, level_text_rect)

    nazad_box = srez_polyg (15, 1200, 35, 180, 100, 'slateblue1')
    nazad_image = pygame.image.load("images/nazad_new.png").convert_alpha()
    nazad_image2 = pygame.transform.scale_by(nazad_image, 1.25)
    screen.blit(nazad_image2, (1210, 45))    
    nazad_string = str(nazad_step)
    nazad_text = pygame.font.Font(None, 120).render(nazad_string, True, 'white')
    screen.blit(nazad_text, (1315, 50))
    nazad_text2 = pygame.font.Font(None, 120).render(nazad_string, True, 'black')
    screen.blit(nazad_text2, (1313, 48))
    
    nazad_price_box = srez_polyg (10, 1170, 105, 80, 60, 'gold')
    nazad_price_string = '-2'
    nazad_price_text = pygame.font.Font(None, 60).render(nazad_price_string, True, 'black')
    nazad_price_text_rect = nazad_price_text.get_rect()
    nazad_price_text_rect.center = nazad_price_box.center
    screen.blit(nazad_price_text, nazad_price_text_rect)
    
    add_kolb_box = srez_polyg (15, 1440, 35, 180, 100, 'slateblue1')
    add_kolb_image = pygame.image.load("images/add_kolb_new.png").convert_alpha()
    add_kolb_image2 = pygame.transform.scale_by(add_kolb_image, 1)
    screen.blit(add_kolb_image2, (1453, 38))
    add_kolb_string = str(add_kolb)
    add_kolb_text = pygame.font.Font(None, 120).render(add_kolb_string, True, 'white')
    screen.blit(add_kolb_text, (1555, 50))
    add_kolb_text = pygame.font.Font(None, 120).render(add_kolb_string, True, 'black')
    screen.blit(add_kolb_text, (1553, 48))
    
    add_kolb_price_box = srez_polyg (10, 1410, 105, 80, 60, 'gold')
    add_kolb_price_string = '-10'
    add_kolb_price_text = pygame.font.Font(None, 60).render(add_kolb_price_string, True, 'black')
    add_kolb_price_text_rect = add_kolb_price_text.get_rect()
    add_kolb_price_text_rect.center = add_kolb_price_box.center
    screen.blit(add_kolb_price_text, add_kolb_price_text_rect)
    
    exit_box = srez_polyg (15, 1680, 35, 180, 100, 'red4')
    exit_string = 'EXIT'
    exit_text = pygame.font.Font(None, 80).render(exit_string, True, 'white')
    exit_text_rect = exit_text.get_rect()
    exit_text_rect.center = exit_box.center
    screen.blit(exit_text, exit_text_rect)
    
    return menu_box, restart_box, points_box, level_box, nazad_box, add_kolb_box, exit_box

# игровые переменные
tube_colors = []
initial_colors = []
boxes = []
new_game = True
selected = False
select_rect = None
level = 1
points = 100
nazad_step = 0
nazad_step_max = 0
nazad_list = []
add_kolb_max = 1
win = False
fact = False
run = True
win_image_scale_rate = 0.0055555555555555555555555555556
win_image_rotate_rate = 0
game_statement = 'game'


while run:
    
    if game_statement == 'approx':
        screen.fill('black')
        win_image = pygame.image.load('images/new_win_srez.png').convert_alpha()
        win_transfor = pygame.transform.scale_by(win_image, win_image_scale_rate)
        win_transfor_2 = pygame.transform.rotate(win_transfor, win_image_rotate_rate)
        rect_win = win_transfor_2.get_rect(center = (WIDTH / 2, HEIGHT / 2))
        screen.blit(win_transfor_2, rect_win)
        win_image_scale_rate += 0.0111111111111111111111111111112
        win_image_rotate_rate -= 4

        if win_image_rotate_rate < -360:
            game_statement = 'win'
        pygame.display.update()
                            
    if game_statement == 'win':

        screen.fill('black')
        
        if not fact:
            facts_line, srez = fact_choice()
            fact = True
        
        srez_polyg (30, 247, 139, 1425, 802, 'orange')
        srez_polyg (25, 247+10, 139+10, 1425-20, 802-20, 'red')
        win_text = pygame.font.Font(None, 400).render('ПОБЕДА!', True, 'white')
        screen.blit(win_text, win_text.get_rect(center=(WIDTH/2 - 1, 309)))
        win_text = pygame.font.Font(None, 400).render('ПОБЕДА!', True, 'gold')
        screen.blit(win_text, win_text.get_rect(center=(WIDTH/2 - 5, 305)))
        
        srez_polyg (20, 305, 460, 1310, 320, 'orange')
        srez_polyg (17, 305+10, 460+10, 1310-20, 320-20, (150, 0, 0))
        
        lines_y_pos = {1: 80, 2: 55, 3: 30, 4: 5, 5: -20, 6: -45} 
        if len(srez) == 0:
            line = ' '.join(facts_line[srez[i]:])
            facts_text = pygame.font.Font(None, 48).render(str(line), True, 'yellow')
            screen.blit(facts_text, facts_text.get_rect(center=(WIDTH/2, HEIGHT/2 + 170)))
        else:
            y = lines_y_pos[len(srez)]
            for i in range(len(srez)):
                if i != len(srez) - 1:
                    line = ' '.join(facts_line[srez[i]:srez[i+1]])
                    facts_text = pygame.font.Font(None, 48).render(str(line), True, 'yellow')
                    screen.blit(facts_text, facts_text.get_rect(center=(WIDTH/2, HEIGHT/2 + y)))
                    y += 50
                else:
                    line = ' '.join(facts_line[srez[i]:])
                    facts_text = pygame.font.Font(None, 48).render(str(line), True, 'yellow')
                    screen.blit(facts_text, facts_text.get_rect(center=(WIDTH/2, HEIGHT/2 + y)))
        
        win_restart_box = srez_polyg (15, 305, 818, 620, 80, "gold")
        win_restart_text = pygame.font.Font(None, 58).render("Пройти уровень еще раз", True, (150, 0, 0))
        win_restart_text_rect = win_restart_text.get_rect()
        win_restart_text_rect.center = win_restart_box.center
        screen.blit(win_restart_text, win_restart_text_rect)
        
        win_new_box = srez_polyg (15, 995, 818, 620, 80, "gold")
        win_new_text = pygame.font.Font(None, 58).render("Начать новый уровень (+5)", True, (150, 0, 0))
        win_new_text_rect = win_new_text.get_rect()
        win_new_text_rect.center = win_new_box.center
        screen.blit(win_new_text, win_new_text_rect)
                    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if win_restart_box.collidepoint(event.pos):
                    tube_colors = copy_list(start_colors)
                    fact = False
                    nazad_step = 0
                    nazad_list = []
                    add_kolb = add_kolb_max
                    game_statement = 'game'
                
                if win_new_box.collidepoint(event.pos):
                    new_game = True
                    fact = False
                    points += 5
                    level += 1
                    nazad_step = 0
                    nazad_list = []
                    add_kolb = add_kolb_max
                    game_statement = 'game'

        pygame.display.update()
    
    
    if game_statement == 'menu':
        screen.fill('black')
               
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
                
        pygame.display.update()
        

    if game_statement == 'game':
        screen.fill('black')
        # generate kolb for new game, make a copy in case of restart
        if new_game:
            fact = False
            tube_colors = no_3_same_parts(level)
            start_colors = copy_list(tube_colors)
            new_game = False
            add_kolb = add_kolb_max
            selected = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Выбор колб для перемещения и отсечение неподходящих ситуаций
                if not selected:
                    for item in range(len(boxes)):
                        if boxes[item].collidepoint(event.pos):
                            # Проверка, если колба полная и заполнена одним цветом, то выделения не произойдет
                            if len (tube_colors[item]) == 4 and same_color(tube_colors[item]):
                                selected = False
                                select_rect = None
                            # ...если колба пустая, выделения тоже не произойдет
                            elif len (tube_colors[item]) == 0:
                                selected = False
                                select_rect = None
                            else:
                                selected = True
                                select_rect = item

                else:
                    for item in range(len(boxes)):
                        if boxes[item].collidepoint(event.pos):
                            dest_rect = item

                            if select_rect != dest_rect:
                                if len(tube_colors[select_rect]) > 0:
                                    if len(tube_colors[dest_rect]) == 0:
                                        nazad_step, nazad_list = prov_perem(select_rect, dest_rect, nazad_step, nazad_step_max, nazad_list)
                                    elif tube_colors[select_rect][-1] == tube_colors[dest_rect][-1]:
                                        nazad_step, nazad_list = prov_perem(select_rect, dest_rect, nazad_step, nazad_step_max, nazad_list)
                                        
                            selected = False
                            select_rect = None
        
        
                if menu_box.collidepoint(event.pos):
                    game_statement = 'menu'

        
                if restart_box.collidepoint(event.pos):
                    tube_colors = copy_list(start_colors)
                    add_kolb = 1
                    nazad_step = 0
                    nazad_list = []
            

                if nazad_box.collidepoint(event.pos):
                    if nazad_step != 0:
                        tube_colors = copy_list(nazad_list[-1])
                        nazad_list.pop(-1)
                        nazad_step -= 1
                        points -= 2
                
                
                if add_kolb_box.collidepoint(event.pos):
                    if add_kolb > 0:
                        if nazad_step < nazad_step_max:
                            nazad_list.append(copy_list(tube_colors))
                            nazad_step += 1
                        else:
                            nazad_list.pop(0)
                            nazad_list.append(copy_list(tube_colors))
                        tube_colors.append([])                
                        add_kolb -= 1
                        points -= 10
                
                
                if exit_box.collidepoint(event.pos):
                    run = False
                    pygame.quit()
                    quit()
                    
                    
        # draw upper line every cycle
        menu_box, restart_box, points_box, level_box, nazad_box, add_kolb_box, exit_box = up_line()
        
        # draw tubes every cycle
        boxes = draw_tubes(tube_colors)
        
        # check for victory every cycle
        win = check_win(tube_colors)
        
        if win:
            win_image_scale_rate = 0.0055555555555555555555555555556
            win_image_rotate_rate = 0
            fade_out(1920, 1080)
            #screen.fill('black')
            game_statement = 'approx'
            
        pygame.display.update()
        


pygame.display.update()
pygame.quit()
