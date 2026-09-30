import pygame
import random

pygame.init()


# Константы
WIDTH = 600
HEIGHT = 400
CELL_SIZE = 20
FPS = 10

# Цвета
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
WHITE = (255, 255, 255)


class Snake:
    def __init__(self):
        self.body = [
            (100, 100),
            (80, 100),
            (60, 100)
        ]
        self.direction = (CELL_SIZE, 0)

    def move(self):
        head_x, head_y = self.body[0]

        new_head = (
            head_x + self.direction[0],
            head_y + self.direction[1]
        )

        self.body.insert(0, new_head)
        self.body.pop()

    def grow(self):
        tail = self.body[-1]
        self.body.append(tail)

    def change_direction(self, new_direction):
        opposite = (
            -self.direction[0],
            -self.direction[1]
        )

        if new_direction != opposite:
            self.direction = new_direction

    def draw(self, screen):
        for segment in self.body:
            pygame.draw.rect(
                screen,
                GREEN,
                (segment[0], segment[1], CELL_SIZE, CELL_SIZE)
            )

    def get_head(self):
        return self.body[0]

    def check_collision(self):
        head = self.get_head()

        # Столкновение со стеной
        if (
            head[0] < 0 or
            head[0] >= WIDTH or
            head[1] < 0 or
            head[1] >= HEIGHT
        ):
            return True

        # Столкновение с собой
        if head in self.body[1:]:
            return True

        return False


class Food:
    def __init__(self, forbidden_positions: list[tuple[int, int]] | None = None):
        self.position = (0, 0)
        self.respawn(forbidden_positions or [])

    def random_position(self, forbidden_positions: list[tuple[int, int]]) -> tuple[int, int]:
        all_positions = [
            (x * CELL_SIZE, y * CELL_SIZE)
            for x in range(WIDTH // CELL_SIZE)
            for y in range(HEIGHT // CELL_SIZE)
            if (x * CELL_SIZE, y * CELL_SIZE) not in forbidden_positions
        ]
        if all_positions:
            return random.choice(all_positions)
        return (0, 0)

    def respawn(self, forbidden_positions: list[tuple[int, int]]):
        self.position = self.random_position(forbidden_positions)

    def draw(self, screen):
        pygame.draw.rect(
            screen,
            RED,
            (
                self.position[0],
                self.position[1],
                CELL_SIZE,
                CELL_SIZE
            )
        )


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode(
            (WIDTH, HEIGHT)
        )

        pygame.display.set_caption("Snake")

        icon = pygame.image.load("icon.png")
        pygame.display.set_icon(icon)

        self.clock = pygame.time.Clock()

        self.snake = Snake()
        self.food = Food(self.snake.body)

        self.score = 0
        self.running = True
        self.game_over = False

        self.font = pygame.font.SysFont(None, 35)

    def handle_events(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_UP:
                    self.snake.change_direction(
                        (0, -CELL_SIZE)
                    )

                elif event.key == pygame.K_DOWN:
                    self.snake.change_direction(
                        (0, CELL_SIZE)
                    )

                elif event.key == pygame.K_LEFT:
                    self.snake.change_direction(
                        (-CELL_SIZE, 0)
                    )

                elif event.key == pygame.K_RIGHT:
                    self.snake.change_direction(
                        (CELL_SIZE, 0)
                    )

                elif event.key == pygame.K_r and self.game_over:
                    self.restart()

    def update(self):
        if self.game_over:
            return

        self.snake.move()

        # Проверка еды
        if self.snake.get_head() == self.food.position:
            self.snake.grow()
            self.food.respawn(self.snake.body)
            self.score += 1

        # Проверка проигрыша
        if self.snake.check_collision():
            self.game_over = True

    def draw(self):
        self.screen.fill(BLACK)

        self.snake.draw(self.screen)
        self.food.draw(self.screen)

        score_text = self.font.render(
            f"Score: {self.score}",
            True,
            WHITE
        )

        self.screen.blit(score_text, (10, 10))

        if self.game_over:
            text = self.font.render(
                "Game over! R - restart",
                True,
                WHITE
            )

            self.screen.blit(
                text,
                (
                    WIDTH // 2 - 150,
                    HEIGHT // 2
                )
            )

        pygame.display.update()

    def restart(self):
        self.snake = Snake()
        self.food = Food(self.snake.body)
        self.score = 0
        self.game_over = False

    def run(self):
        while self.running:

            self.handle_events()
            self.update()
            self.draw()

            self.clock.tick(FPS)

        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()