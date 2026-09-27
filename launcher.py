import pygame
from pathlib import Path
from typing import Any, Sequence
import json
import subprocess
import sys

CARD_X = 300
CARD_Y = 500
CARD_INDENT = 25
GAMES_DIR = Path("games")


class Game:
    def __init__(self, path: Path, metadata: dict[str, Any]) -> None:
        self.path = path
        self.metadata = metadata

        self.name = metadata.get("name")
        self.author = metadata.get("author")
        self.description = metadata.get("description")
        self.icon = metadata.get("icon")
        self.version = metadata.get("version")
        self.entry_point = metadata.get("entry_point", "main.py")

    def launch(self) -> None:
        subprocess.run([sys.executable, self.entry_point], cwd=str(self.path))


class Card:
    ICON_SIZE = 250
    INDENT = 25
    FONT_NAME = "Arial"
    NAME_FONT_SIZE = 48
    AUTHOR_FONT_SIZE = 24
    DESCRIPTION_FONT_SIZE = 20
    TEXT_COLOR = (255, 255, 255)

    def __init__(self, rect: pygame.Rect, game: Game) -> None:
        self.game = game
        self.rect = rect
        self.name = game.name
        self.author = game.author
        self.description = game.description

        icon_path = game.path / game.icon
        self.icon_image = pygame.transform.scale(
            pygame.image.load(str(icon_path)), 
            (self.ICON_SIZE, self.ICON_SIZE)
        )

    def draw(self, screen: pygame.Surface) -> None:
        # Оптимизировать создание текста; вынести его в класс
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

    def handle_click(self, pos: tuple[int, int] | Sequence[int]) -> bool:
        if self.rect.collidepoint(pos):
            self.game.launch()
            return True
        return False


class Menu:
    def __init__(self, width: int = 1000, height: int = 800) -> None:
        self.width = width
        self.height = height
        self.clock = pygame.time.Clock()
        self.games = self.discover_games()
        self.cards = self.get_cards()

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Pygame Collab")

    def discover_games(self) -> list[Game]:
        games = []

        for path in GAMES_DIR.iterdir():
            if not path.is_dir():
                continue

            metadata_path = path / "metadata.json"

            if not metadata_path.exists():
                continue

            try:
                metadata = json.loads(metadata_path.read_text(encoding="utf-8"))

                game = Game(path, metadata)

                games.append(game)

            except Exception as e:
                print(f"Failed to load {path.name}: {e}")

        return games

    @classmethod
    def get_card_rect(cls, num: int) -> pygame.Rect:
        card_x = num % 3 * (CARD_X + CARD_INDENT) + CARD_INDENT
        card_y = num // 3 * (CARD_Y + CARD_INDENT) + CARD_INDENT

        return pygame.rect.Rect(card_x, card_y, CARD_X, CARD_Y)

    def get_cards(self) -> list[Card]:
        cards = []

        for num, game in enumerate(self.games):
            card_rect = self.get_card_rect(num)

            cards.append(Card(card_rect, game))

        return cards

    def draw_cards(self) -> None:
        for card in self.cards:
            card.draw(self.screen)

    def check_card_click(self, event: pygame.event.Event) -> None:
        for card in self.cards:
            if card.handle_click(event.pos):
                pygame.event.clear()
                break

    def handle_events(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONUP:
                self.check_card_click(event)

        return True

    def run(self) -> None:
        begin = True

        while begin:
            self.screen.fill((200, 200, 200))
            begin = self.handle_events()

            self.draw_cards()

            pygame.display.update()
            self.clock.tick(60)


menu = Menu()