import pygame

width = 1200
height = 800
clock = pygame.time.Clock()

pygame.init()

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("4 in a row")

balls_positions = [["empty" for i in range(6)] for i in range(7)]

cellsize = 100
move_player = 1
pos_x, pos_y = (600, 100)
ball_pos = ((pos_x + 50) // cellsize * cellsize, 100)
check_win_moves = (
    ((0, 0), (-1, 0), (-2, 0), (-3, 0)), ((1, 0), (0, 0), (-1, 0), (-2, 0)), ((2, 0), (1, 0), (0, 0), (-1, 0)), ((3, 0), (2, 0), (1, 0), (0, 0)),
    ((0, 0), (0, -1), (0, -2), (0, -3)), ((0, 1), (0, 0), (0, -1), (0, -2)), ((0, 2), (0, 1), (0, 0), (0, -1)), ((0, 3), (0, 2), (0, 1), (0, 0)),
    ((0, 0), (-1, -1), (-2, -2), (-3, -3)), ((1, 1), (0, 0), (-1, -1), (-2, -2)), ((2, 2), (1, 1), (0, 0), (-1, -1)), ((3, 3), (2, 2), (1, 1), (0, 0)),
    ((0, 0), (1, -1), (2, -2), (3, -3)), ((-1, 1), (0, 0), (1, -1), (2, -2)), ((-2, 2), (-1, 1), (0, 0), (1, -1)), ((-3, 3), (-2, 2), (-1, 1), (0, 0))
)
slide = False
gravity = 0.6
elasticity = 0.4
slide = {}
move_state = True

def menu():
    # Simple start menu with two options: 1vs1 and CPU
    font_title = pygame.font.Font(None, 96)
    font_button = pygame.font.Font(None, 40)

    button_w, button_h = 500, 90
    center_x = width // 2
    start_y = height // 2 - 80

    btn1_rect = pygame.Rect(0, 0, button_w, button_h)
    btn1_rect.center = (center_x, start_y)
    btn2_rect = pygame.Rect(0, 0, button_w, button_h)
    btn2_rect.center = (center_x, start_y + 140)

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_pressed = True
            if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                pygame.quit()
                raise SystemExit

        screen.fill((30, 30, 40))

        # Title
        title_surf = font_title.render("4 в ряд", True, (245, 245, 245))
        title_rect = title_surf.get_rect(center=(center_x, height // 4))
        screen.blit(title_surf, title_rect)

        # Button 1 (1 vs 1)
        hovered1 = btn1_rect.collidepoint(mouse_pos)
        color1 = (240, 120, 90) if hovered1 else (220, 80, 60)
        pygame.draw.rect(screen, color1, btn1_rect, border_radius=16)
        text1 = font_button.render("Играть с другом (1vs1)", True, (255, 255, 255))
        text1_rect = text1.get_rect(center=btn1_rect.center)
        screen.blit(text1, text1_rect)

        # Button 2 (CPU)
        hovered2 = btn2_rect.collidepoint(mouse_pos)
        color2 = (80, 130, 240) if hovered2 else (60, 110, 220)
        pygame.draw.rect(screen, color2, btn2_rect, border_radius=16)
        text2 = font_button.render("Играть с ботом (CPU)", True, (255, 255, 255))
        text2_rect = text2.get_rect(center=btn2_rect.center)
        screen.blit(text2, text2_rect)

        # Subtle caption
        caption = pygame.font.Font(None, 22).render("Нажмите кнопку для начала", True, (200, 200, 200))
        screen.blit(caption, (center_x - caption.get_width() // 2, start_y + 260))

        if mouse_pressed:
            if hovered1:
                return "1vs1"
            if hovered2:
                return "cpu"

        pygame.display.update()
        clock.tick(60)

def move_down_ball():
    pass

def draw_ball(move_player, cords):
    pygame.draw.circle(screen, (0, 0, 0), cords, 48)
    pygame.draw.circle(screen, (255, 0, 0) if move_player else (0, 0, 255), cords, 40)

def check_for_win(col, row):
    for index_move in range(len(check_win_moves)):
        check_for_red_win = 0
        check_for_blue_win = 0
        for index_move_2, move_2 in enumerate(check_win_moves[index_move]):
            if col + move_2[0] < 0 or row + move_2[1] < 0:
                break
            try:
                if balls_positions[row // cellsize - 3 + move_2[0]][5 - col + move_2[1]] == 1:
                    check_for_red_win += 1
                    if check_for_red_win == 4:
                        print("Красный выиграл!")
                elif balls_positions[row // cellsize - 3 + move_2[0]][5 - col + move_2[1]] == 0:
                    check_for_blue_win += 1
                    if check_for_blue_win == 4:
                        print("Синий выиграл!")
            except IndexError:
                break

# show menu and get selected mode (not used further here)
selected_mode = menu()

begin = True
while begin:
    screen.fill((255, 115, 115) if move_player else (115, 115, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            begin = False
            pygame.quit()
        if event.type == pygame.MOUSEMOTION:
            pos_x, pos_y = event.pos
            ball_pos = ((pos_x + 50) // cellsize * cellsize, 100)
        if event.type == pygame.MOUSEBUTTONUP:
            if ball_pos[0] > 200 and ball_pos[0] < 1000:
                for ind, i in enumerate(balls_positions[ball_pos[0] // cellsize - 3][::-1]):
                    if i == "empty" and move_state:
                        slide = {"stop_y": (5 - ind) * cellsize + 250 - 1, "pos_x": ball_pos[0], "move": 100, "color": move_player, "velosity": 0, "insert_ball": (ball_pos[0] // cellsize - 3, 5 - ind), "ind": ind}
                        move_player = 0 if move_player else 1
                        break

    pygame.draw.rect(screen, (20, 20, 20), (200, 150, 800, 700), 0, cellsize // 2)

    if ball_pos[0] > 200 and ball_pos[0] < 1000:
        draw_ball(move_player, ball_pos)
    else:
        if ball_pos[0] <= 200:
            draw_ball(move_player, (300, 100))
        elif ball_pos[0] >= 1000:
            draw_ball(move_player, (900, 100))

    for ind, i in enumerate(balls_positions):
        for jnd, j in enumerate(balls_positions[ind]):
            if j == "empty":
                pygame.draw.rect(screen, (50, 50, 50), (250 + ind * cellsize + 2, 200 + jnd * cellsize, cellsize - 4, cellsize - 4), 0, cellsize // 2)
            elif j == 1:
                draw_ball(1, (300 + ind * cellsize, 250 + jnd * cellsize))
            elif j == 0:
                draw_ball(0, (300 + ind * cellsize, 250 + jnd * cellsize))

    if ball_pos[0] > 200 and ball_pos[0] < 1000:
        for ind, i in enumerate(balls_positions[ball_pos[0] // cellsize - 3][::-1]):
            if i == "empty":
                pygame.draw.circle(screen, (100, 100, 100), (ball_pos[0], (5 - ind) * cellsize + 248), 48)

    if slide:
        move_state = False
        slide["velosity"] = gravity + slide["velosity"]
        slide["move"] = slide["velosity"] + slide["move"]

        if slide["move"] > slide["stop_y"]:
            slide["move"] = slide["stop_y"]
            slide["velosity"] = -slide["velosity"] * elasticity

            if abs(slide["velosity"]) < 0.5:
                slide["velosity"] = 0
                slide["move"] = slide["stop_y"]
                balls_positions[slide["insert_ball"][0]][slide["insert_ball"][1]] = slide["color"]
                check_for_win(slide["ind"], slide["pos_x"])
                slide.clear()
                move_state = True
                continue
        draw_ball(slide["color"], (slide["pos_x"], slide["move"]))

    pygame.display.update()
    clock.tick(60)