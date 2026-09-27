import pygame
from pathlib import Path
import importlib
import json

CARD_X = 300
CARD_Y = 500
CARD_INDENT = 25
GAMES_DIR = Path("games")


class Game:
    def __init__(self, module, path, metadata):
        self.module = module
        self.path = path
        self.metadata = metadata

        self.name = metadata.get("name")
        self.author = metadata.get("author")
        self.description = metadata.get("description")
        self.icon = metadata.get("icon")
        self.version = metadata.get("version")


class Card:
    ICON_SIZE = 250
    INDENT = 25
    FONT_NAME = "Arial"
    NAME_FONT_SIZE = 48
    AUTHOR_FONT_SIZE = 24
    DESCRIPTION_FONT_SIZE = 20
    TEXT_COLOR = (255, 255, 255)

    def __init__(self, icon, name, author, description, rect):
        self.icon = icon
        self.name = name
        self.author = author
        self.description = description
        self.rect = rect

        self.icon_image = pygame.transform.scale(pygame.image.load(icon), (self.ICON_SIZE, self.ICON_SIZE))

    def draw(self, screen):
        pygame.draw.rect(screen, (50, 50, 50), self.rect, border_radius=10)

        icon = self.icon_image
        screen.blit(icon, (self.rect.x + self.INDENT, self.rect.y + self.INDENT))

        # Render fonts amd texts
        name_font = pygame.font.SysFont(self.FONT_NAME, self.NAME_FONT_SIZE)
        name_text = name_font.render(self.name, 1, self.TEXT_COLOR)

        author_font = pygame.font.SysFont(self.FONT_NAME, self.AUTHOR_FONT_SIZE)
        author_text = author_font.render("by " + self.author, 1, self.TEXT_COLOR)

        description_font = pygame.font.SysFont(self.FONT_NAME, self.DESCRIPTION_FONT_SIZE)
        description_text = description_font.render(self.description, 1, self.TEXT_COLOR)

        rect_center = CARD_X // 2 + self.rect.x

        # Center the rects
        name_rect = name_text.get_rect(center=(rect_center, self.rect.y + 320))
        author_rect = author_text.get_rect(center=(rect_center, self.rect.y + 370))
        description_rect = description_text.get_rect(center=(rect_center, self.rect.y + 400))

        # Blit texts
        screen.blit(name_text, name_rect)
        screen.blit(author_text, author_rect)
        screen.blit(description_text, description_rect)


class Menu:
    def __init__(self, width: int = 1000, height: int = 800):
        self.width = width
        self.height = height
        self.clock = pygame.time.Clock()

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Pygame Collab")

    def discover_games(self):
        games = []

        for path in GAMES_DIR.iterdir():
            if not path.is_dir():
                continue

            metadata_path = path / "metadata.json"

            if not metadata_path.exists():
                continue

            try:
                metadata = json.loads(metadata_path.read_text(encoding="utf-8"))

                module = importlib.import_module(f"games.{path.name}")

                game = Game(module, path, metadata)

                games.append(game)

            except Exception as e:
                print(f"Failed to load {path.name}: {e}")

        return games

    @classmethod
    def get_card_rect(cls, num):
        card_x = num % 3 * (CARD_X + CARD_INDENT) + CARD_INDENT
        card_y = num // 3 * (CARD_Y + CARD_INDENT) + CARD_INDENT

        return pygame.rect.Rect(card_x, card_y, CARD_X, CARD_Y)

    def draw_cards(self):
        games = self.discover_games()

        for num, game in enumerate(games):
            path = str(game.path)
            name, author, description = game.name, game.author, game.description
            icon = game.icon

            icon_path = path + "/" + icon

            card_rect = self.get_card_rect(num)

            card = Card(icon_path, name, author, description, card_rect)

            card.draw(self.screen)

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

            self.draw_cards()

            pygame.display.update()
            self.clock.tick(60)

menu = Menu()