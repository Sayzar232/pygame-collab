import pygame
import random
import sys

# ----------------------------
# Настройки
# ----------------------------
CELL = 50
COLS = 10
ROWS = 20

WIDTH = COLS * CELL
HEIGHT = ROWS * CELL

FPS = 60
FALL_SPEED = 500  # миллисекунды

# Цвета
BLACK = (15, 15, 20)
WHITE = (240, 240, 240)
GRAY = (45, 45, 55)

COLORS = [
    (0, 240, 240),    # I
    (0, 100, 240),    # J
    (240, 160, 0),    # L
    (240, 240, 0),    # O
    (0, 220, 80),     # S
    (160, 0, 240),    # T
    (240, 50, 50),    # Z
]

# Фигуры
SHAPES = [
    [[1, 1, 1, 1]],

    [[1, 0, 0],
     [1, 1, 1]],

    [[0, 0, 1],
     [1, 1, 1]],

    [[1, 1],
     [1, 1]],

    [[0, 1, 1],
     [1, 1, 0]],

    [[0, 1, 0],
     [1, 1, 1]],

    [[1, 1, 0],
     [0, 1, 1]],
]


# ----------------------------
# Функции
# ----------------------------
def rotate(shape):
    """Поворот матрицы на 90 градусов."""
    return [list(row) for row in zip(*shape[::-1])]


def new_piece():
    index = random.randrange(len(SHAPES))

    return {
        "shape": [row[:] for row in SHAPES[index]],
        "color": COLORS[index],
        "x": COLS // 2 - len(SHAPES[index][0]) // 2,
        "y": 0,
    }


def valid_position(board, piece):
    """Проверяет, можно ли разместить фигуру."""
    shape = piece["shape"]

    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if not cell:
                continue

            board_x = piece["x"] + x
            board_y = piece["y"] + y

            if board_x < 0 or board_x >= COLS:
                return False

            if board_y >= ROWS:
                return False

            if board_y >= 0 and board[board_y][board_x] is not None:
                return False

    return True


def lock_piece(board, piece):
    """Фиксирует фигуру на игровом поле."""
    for y, row in enumerate(piece["shape"]):
        for x, cell in enumerate(row):
            if cell:
                board_y = piece["y"] + y
                board_x = piece["x"] + x

                if 0 <= board_y < ROWS:
                    board[board_y][board_x] = piece["color"]


def clear_lines(board):
    """Удаляет заполненные линии и возвращает количество удалённых."""
    new_board = [
        row for row in board
        if any(cell is None for cell in row)
    ]

    lines = ROWS - len(new_board)

    while len(new_board) < ROWS:
        new_board.insert(0, [None] * COLS)

    board[:] = new_board

    return lines


def draw_cell(screen, x, y, color):
    """Рисует одну клетку."""
    rect = pygame.Rect(
        x * CELL,
        y * CELL,
        CELL,
        CELL
    )

    pygame.draw.rect(screen, color, rect)
    pygame.draw.rect(screen, GRAY, rect, 1)


def draw_board(screen, board):
    """Рисует игровое поле."""
    for y in range(ROWS):
        for x in range(COLS):
            if board[y][x] is not None:
                draw_cell(screen, x, y, board[y][x])


def draw_piece(screen, piece):
    """Рисует текущую фигуру."""
    for y, row in enumerate(piece["shape"]):
        for x, cell in enumerate(row):
            if cell:
                draw_cell(
                    screen,
                    piece["x"] + x,
                    piece["y"] + y,
                    piece["color"]
                )


def draw_grid(screen):
    """Рисует сетку."""
    for x in range(COLS + 1):
        pygame.draw.line(
            screen,
            GRAY,
            (x * CELL, 0),
            (x * CELL, HEIGHT)
        )

    for y in range(ROWS + 1):
        pygame.draw.line(
            screen,
            GRAY,
            (0, y * CELL),
            (WIDTH, y * CELL)
        )


def draw_text(screen, text, size, y):
    font = pygame.font.Font(None, size)
    surface = font.render(text, True, WHITE)

    rect = surface.get_rect(
        center=(WIDTH // 2, y)
    )

    screen.blit(surface, rect)


# ----------------------------
# Игра
# ----------------------------
def main():
    pygame.init()

    screen = pygame.display.set_mode(
        (WIDTH, HEIGHT)
    )

    pygame.display.set_caption("Tetris")

    clock = pygame.time.Clock()

    board = [
        [None for _ in range(COLS)]
        for _ in range(ROWS)
    ]

    piece = new_piece()

    score = 0
    fall_timer = 0

    running = True
    game_over = False

    while running:
        dt = clock.tick(FPS)
        fall_timer += dt

        # ------------------------
        # События
        # ------------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:

                if game_over:
                    if event.key == pygame.K_r:
                        board = [
                            [None for _ in range(COLS)]
                            for _ in range(ROWS)
                        ]

                        piece = new_piece()
                        score = 0
                        fall_timer = 0
                        game_over = False

                    elif event.key == pygame.K_ESCAPE:
                        running = False

                    continue

                # Влево
                if event.key == pygame.K_LEFT:
                    piece["x"] -= 1

                    if not valid_position(board, piece):
                        piece["x"] += 1

                # Вправо
                elif event.key == pygame.K_RIGHT:
                    piece["x"] += 1

                    if not valid_position(board, piece):
                        piece["x"] -= 1

                # Мягкое падение
                elif event.key == pygame.K_DOWN:
                    piece["y"] += 1

                    if not valid_position(board, piece):
                        piece["y"] -= 1

                # Поворот
                elif event.key == pygame.K_UP:
                    old_shape = piece["shape"]

                    piece["shape"] = rotate(
                        piece["shape"]
                    )

                    if not valid_position(board, piece):
                        piece["shape"] = old_shape

                # Мгновенное падение
                elif event.key == pygame.K_SPACE:
                    while True:
                        piece["y"] += 1

                        if not valid_position(board, piece):
                            piece["y"] -= 1
                            break

                    lock_piece(board, piece)

                    lines = clear_lines(board)

                    score += {
                        1: 100,
                        2: 300,
                        3: 500,
                        4: 800,
                    }.get(lines, 0)

                    piece = new_piece()

                    if not valid_position(board, piece):
                        game_over = True

                    fall_timer = 0

        # ------------------------
        # Автоматическое падение
        # ------------------------
        if not game_over and fall_timer >= FALL_SPEED:
            fall_timer = 0

            piece["y"] += 1

            if not valid_position(board, piece):
                piece["y"] -= 1

                lock_piece(board, piece)

                lines = clear_lines(board)

                score += {
                    1: 100,
                    2: 300,
                    3: 500,
                    4: 800,
                }.get(lines, 0)

                piece = new_piece()

                if not valid_position(board, piece):
                    game_over = True

        # ------------------------
        # Рисование
        # ------------------------
        screen.fill(BLACK)

        draw_board(screen, board)
        draw_grid(screen)

        if not game_over:
            draw_piece(screen, piece)

        # Счёт
        font = pygame.font.Font(None, 26)
        score_text = font.render(
            f"Score: {score}",
            True,
            WHITE
        )

        screen.blit(
            score_text,
            (5, 5)
        )

        # Game Over
        if game_over:
            overlay = pygame.Surface(
                (WIDTH, HEIGHT),
                pygame.SRCALPHA
            )

            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))

            draw_text(
                screen,
                "GAME OVER",
                48,
                HEIGHT // 2 - 40
            )

            draw_text(
                screen,
                "Press R to restart",
                28,
                HEIGHT // 2 + 10
            )

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()