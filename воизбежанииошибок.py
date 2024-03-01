import pygame
import random
from sound import bgmusic
import sys

# Начальные настройки
pygame.init()
WIDTH = 1000
HEIGHT = 700
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('2048')  # заголовок окошка
timer = pygame.time.Clock()
fps = 60
font = pygame.font.Font('freesansbold.ttf', 24)
background_image = pygame.image.load("1613164641_71-p-zheltii-fon-kvadratnii-88.png").convert()


# Библиотека цветов 2048
colors = {0: (204, 192, 179),
          2: (238, 228, 218),
          4: (237, 224, 200),
          8: (242, 177, 121),
          16: (245, 149, 99),
          32: (246, 124, 95),
          64: (246, 94, 59),
          128: (237, 207, 114),
          256: (237, 204, 97),
          512: (237, 200, 80),
          1024: (237, 197, 63),
          2048: (237, 194, 46),
          'light text': (249, 246, 242),
          'dark text': (119, 110, 101),
          'other': (0, 0, 0),
          'bg': (255, 250, 195)}

# Игровые переменные
board_values = [[0 for _ in range(4)] for _ in range(4)]
game_over = False
spawn_new = True
init_count = 0
direction = ''
score = 0
file = open('high_score', 'r')
init_high = int(file.readline())
file.close()
high_score = init_high
message_list = ["Nice!", "Excellent!", "Wow!", "Good!", "Super!"]
current_message = ""
message_timer = 0

main_menu_button_rect = pygame.Rect(WIDTH - 100, HEIGHT - 110, 100, 50)
exit_button_rect = pygame.Rect(WIDTH - 100, HEIGHT - 50, 100, 50)

game_active = False


def main_menu():
    menu_font = pygame.font.Font('freesansbold.ttf', 36)
    menu_text1 = menu_font.render('2048 Game', True, 'black')
    start_button_rect = pygame.Rect(WIDTH // 2 - 75, 300, 150, 50)
    exit_button_rect = pygame.Rect(WIDTH // 2 - 75, 400, 150, 50)

    while True:
        screen.fill(colors['bg'])
        screen.blit(menu_text1, (WIDTH // 2 - menu_text1.get_width() // 2, 200))

        # Рисуем кнопку "Start"
        pygame.draw.rect(screen, (255, 255, 255), start_button_rect)
        start_text = font.render("Start", True, 'black')
        screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, 315))
        pygame.draw.rect(screen, 'black', start_button_rect, 2, 5)

        # Рисуем кнопку "Exit"
        pygame.draw.rect(screen, (255, 255, 255), exit_button_rect)
        exit_text = font.render("Exit", True, 'black')
        screen.blit(exit_text, (WIDTH // 2 - exit_text.get_width() // 2, 415))
        pygame.draw.rect(screen, 'black', exit_button_rect, 2, 5)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if start_button_rect.collidepoint(mouse_pos):
                    return True  # Нажата кнопка "Start", выходим из меню
                elif exit_button_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()


# Окошко проигрыша и рестарт



def draw_over():
    pygame.draw.rect(screen, 'black', [70, 70, 420, 140], 0, 10)
    game_over_text1 = font.render('Game Over!', True, 'white')
    game_over_text2 = font.render('Press Enter to Restart!', True, 'white')
    screen.blit(game_over_text1, (200, 91))
    screen.blit(game_over_text2, (150, 147))

    for event in pygame.event.get():
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RETURN:
                # Обновляем игровую доску и сбрасываем счет
                global board_values, spawn_new, init_count, score, direction, game_over
                board_values = [[0 for _ in range(4)] for _ in range(4)]
                spawn_new = True
                init_count = 0
                score = 0
                direction = ''
                game_over = False


# Движение
def take_turn(direc, board):
    global score
    merged = [[False for _ in range(4)] for _ in range(4)]
    if direc == 'UP':
        for i in range(4):
            for j in range(4):
                shift = 0
                if i > 0:
                    for q in range(i):
                        if board[q][j] == 0:
                            shift += 1
                    if shift > 0:
                        board[i - shift][j] = board[i][j]
                        board[i][j] = 0
                    if board[i - shift - 1][j] == board[i - shift][j] and not merged[i - shift - 1][j] \
                            and not merged[i - shift][j]:
                        board[i - shift - 1][j] *= 2
                        score += board[i - shift - 1][j]
                        board[i - shift][j] = 0
                        merged[i - shift - 1][j] = True
    elif direc == 'DOWN':
        for i in range(3):
            for j in range(4):
                shift = 0
                for q in range(i + 1):
                    if board[3 - q][j] == 0:
                        shift += 1
                if shift > 0:
                    board[2 - i + shift][j] = board[2 - i][j]
                    board[2 - i][j] = 0
                if 3 - i + shift <= 3:
                    if board[2 - i + shift][j] == board[3 - i + shift][j] and not merged[3 - i + shift][j] \
                            and not merged[2 - i + shift][j]:
                        board[3 - i + shift][j] *= 2
                        score += board[3 - i + shift][j]
                        board[2 - i + shift][j] = 0
                        merged[3 - i + shift][j] = True

    elif direc == 'LEFT':
        for i in range(4):
            for j in range(4):
                shift = 0
                for q in range(j):
                    if board[i][q] == 0:
                        shift += 1
                if shift > 0:
                    board[i][j - shift] = board[i][j]
                    board[i][j] = 0
                if board[i][j - shift] == board[i][j - shift - 1] and not merged[i][j - shift - 1] \
                        and not merged[i][j - shift]:
                    board[i][j - shift - 1] *= 2
                    score += board[i][j - shift - 1]
                    board[i][j - shift] = 0
                    merged[i][j - shift - 1] = True

    elif direc == 'RIGHT':
        for i in range(4):
            for j in range(4):
                shift = 0
                for q in range(j):
                    if board[i][3 - q] == 0:
                        shift += 1
                if shift > 0:
                    board[i][3 - j + shift] = board[i][3 - j]
                    board[i][3 - j] = 0
                if 4 - j + shift <= 3:
                    if board[i][4 - j + shift] == board[i][3 - j + shift] and not merged[i][4 - j + shift] \
                            and not merged[i][3 - j + shift]:
                        board[i][4 - j + shift] *= 2
                        score += board[i][4 - j + shift]
                        board[i][3 - j + shift] = 0
                        merged[i][4 - j + shift] = True
    return board


# Спавн рандомных прямоугольничков
def new_pieces(board):
    count = 0
    full = False
    while any(0 in row for row in board) and count < 1:
        row = random.randint(0, 3)
        col = random.randint(0, 3)
        if board[row][col] == 0:
            count += 1
            if random.randint(1, 10) == 10:
                board[row][col] = 4
            else:
                board[row][col] = 2
    if count < 1:
        full = True
    return board, full


# Фон для игровой доски
def draw_board():
    pygame.draw.rect(screen, (255, 250, 170), [0, 0, 560, 560], 0)

    pygame.draw.rect(screen, (0, 0, 0), [0, 0, 560, 560], 5)

    score_text = font.render(f'Score: {score}', True, 'black')
    high_score_text = font.render(f'High Score: {high_score}', True, 'black')
    screen.blit(score_text, (14, 574))
    screen.blit(high_score_text, (14, 630))


# Текст и цифры для игры


def draw_pieces(board):
    for i in range(4):
        for j in range(4):
            value = board[i][j]
            if value > 8:
                value_color = colors['light text']
            else:
                value_color = colors['dark text']
            if value <= 2048:
                color = colors[value]
            else:
                color = colors['other']
            pygame.draw.rect(screen, color, [j * 133 + 28, i * 133 + 28, 105, 105], 0, 5)
            if value > 0:
                value_len = len(str(value))
                font = pygame.font.Font('freesansbold.ttf', 48 - (5 * value_len))
                value_text = font.render(str(value), True, value_color)
                text_rect = value_text.get_rect(center=(j * 133 + 80, i * 133 + 80))
                screen.blit(value_text, text_rect)
                # Контур для прямоугольничков
                pygame.draw.rect(screen, 'black', [j * 133 + 28, i * 133 + 28, 105, 105], 2, 5)


def display_message(message):
    message_font = pygame.font.Font(pygame.font.match_font('comicsansms'), 45)
    message_surface = message_font.render(message, True, (50, 205, 50))
    message_rect = message_surface.get_rect(center=(780, 100))
    screen.blit(message_surface, message_rect.move(0, -50))
    pygame.display.flip()


def draw_over():
    pygame.draw.rect(screen, 'black', [70, 70, 420, 140], 0, 10)
    game_over_text1 = font.render('Game Over!', True, 'white')
    game_over_text2 = font.render('Press Enter to Restart!', True, 'white')
    screen.blit(game_over_text1, (200, 91))
    screen.blit(game_over_text2, (150, 147))
    pygame.display.flip()

# Главный игровой цикл
run = True
bgmusic()
show_message = False
show_message_start_time = 0

while run:
    if not game_active:
        game_active = main_menu()
        if not game_active:
            pygame.quit()
            sys.exit()

    timer.tick(fps)
    screen.blit(background_image, (0, 0))
    draw_board()
    draw_pieces(board_values)

    # Отрисовка кнопок "Exit" и "Main Menu"
    pygame.draw.rect(screen, (255, 255, 255), exit_button_rect)
    exit_text = font.render("Exit", True, 'black')
    screen.blit(exit_text, (WIDTH - 53 - exit_text.get_width() // 2, HEIGHT - 38))
    pygame.draw.rect(screen, 'black', exit_button_rect, 2, 5)

    pygame.draw.rect(screen, (255, 255, 255), main_menu_button_rect)
    main_menu_text = font.render("Menu", True, 'black')
    screen.blit(main_menu_text, (WIDTH - 50 - main_menu_text.get_width() // 2, HEIGHT - 98))
    pygame.draw.rect(screen, 'black', main_menu_button_rect, 2, 5)

    if spawn_new or init_count < 2:
        board_values, game_over = new_pieces(board_values)
        spawn_new = False
        init_count += 1

    if direction != '':
        board_values = take_turn(direction, board_values)
        direction = ''
        spawn_new = True

    if score % 10 == 0 and score != 0 and not show_message:
        current_message = random.choice(message_list)
        show_message = True
        show_message_start_time = pygame.time.get_ticks()

    if game_over:
        draw_over()
        if high_score > init_high:
            file = open('high_score', 'w')
            file.write(f'{high_score}')
            file.close()
            init_high = high_score

        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN:
                    # Рестарт игры
                    board_values = [[0 for _ in range(4)] for _ in range(4)]
                    spawn_new = True
                    init_count = 0
                    score = 0
                    direction = ''
                    game_over = False

    if show_message:
        display_message(current_message)
        current_time = pygame.time.get_ticks()
        if current_time - show_message_start_time > 2000:  # 2000 миллисекунд (2 секунды)
            show_message = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                direction = 'UP'
            elif event.key == pygame.K_DOWN:
                direction = 'DOWN'
            elif event.key == pygame.K_LEFT:
                direction = 'LEFT'
            elif event.key == pygame.K_RIGHT:
                direction = 'RIGHT'
            if game_over:
                draw_over()
                if high_score > init_high:
                    file = open('high_score', 'w')
                    file.write(f'{high_score}')
                    file.close()
                    init_high = high_score

        # Проверка на щелчок мыши по кнопкам
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if exit_button_rect.collidepoint(mouse_pos):
                pygame.quit()
                sys.exit()
            elif main_menu_button_rect.collidepoint(mouse_pos):
                game_active = False

    if score > high_score:
        high_score = score

    pygame.display.flip()

pygame.quit()
