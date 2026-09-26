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
        self._module = module
        self._path = path
        self._metadata = metadata

    @property
    def module(self):
        return self._module

    @property
    def path(self):
        return self._path

    @property
    def metadata(self):
        metadata = self._metadata
        name, author, description = metadata.get("name"), metadata.get("author"), metadata.get("description")
        icon = metadata.get("icon")
        version = metadata.get("version")

        return name, author, description, icon, version

class Card:
    def __init__(self, icon, name, author, description, num):
        self.icon = icon
        self.name = name
        self.author = author
        self.description = description
        self.num = num

    def draw(self, screen):
        icon = pygame.image.load(self.icon)
        icon = pygame.transform.scale(icon, (CARD_X, CARD_Y))
        
        card_dx = self.num % 3 * CARD_X
        card_dy = self.num // 3 * CARD_Y
        pygame.draw.rect(screen, (50, 50, 50), (CARD_INDENT + card_dx, CARD_INDENT + card_dy, CARD_X, CARD_Y), border_radius=10)


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

    def draw_game_card(self, icon, name, author, description, num):
        icon = pygame.image.load(icon)
        icon = pygame.transform.scale(icon, (CARD_X, CARD_Y))

        card_dx = num % 3 * CARD_X
        card_dy = num // 3 * CARD_Y
        pygame.draw.rect(self.screen, (50, 50, 50), (CARD_INDENT + card_dx, CARD_INDENT + card_dy, CARD_X, CARD_Y), border_radius=10)

    def draw_cards(self):
        games = self.discover_games()

        for num, game in enumerate(games):
            path = str(game.path)
            name, author, description, icon, version = game.metadata
            icon_path = path + "/" + icon

            card = Card(icon_path, name, author, description, num)

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