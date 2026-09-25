import pygame

pygame.init()

CARD_X = 300
CARD_Y = 500


class Game:
    def __init__(self, width: int = 1000, height: int = 800):
        self.width = width
        self.height = height
        self.clock = pygame.time.Clock()

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Pygame Collab")

    def draw_game_card(self, icon):
        icon = pygame.transform.scale(icon, (CARD_X, CARD_Y))
        pygame.draw.rect(self.screen, (50, 50, 50), (30, 30, CARD_X, CARD_Y), border_radius=10)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        return True

    def run(self):
        begin = True
        while begin:
            self.screen.fill((200, 200, 200))
            begin = self.handle_events()

            pygame.display.update()
            self.clock.tick(60)

if __name__ == "__main__":
    game = Game()
    game.run()

    pygame.quit()