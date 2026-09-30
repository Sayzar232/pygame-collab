import pygame
from pathlib import Path
from typing import Any, Sequence
from dataclasses import dataclass
import json
import subprocess
import sys
import logging

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
logger = logging.getLogger("Launcher")

CARD_X = 300
CARD_Y = 500
CARD_INDENT = 25
SCROLL_SPEED = 15
GAMES_DIR = Path("games")
PLACEHOLER_ICON = "placeholder_icon"


@dataclass
class GameMetadata:
    name: str
    author: str
    description: str
    icon: str
    entry_point: str
    version: str = "1.0.0"

    @classmethod
    def from_dict(cls, data: Any, base_dir: Path) -> "GameMetadata":
        if not isinstance(data, dict):
            raise ValueError(f"Метаданные должны быть JSON-объектом, получено: {type(data).__name__}")

        required_fields = ["name", "author", "description"]
        for field in required_fields:
            val = data.get(field)
            if val is None or not isinstance(val, str) or not val.strip():
                raise ValueError(f"Поле '{field}' обязательно и должно быть непустой строкой")

        name = data["name"].strip()
        author = data["author"].strip()
        description = data["description"].strip()

        entry_point = data.get("entry_point", "main.py")
        if not isinstance(entry_point, str) or not entry_point.strip():
            raise ValueError("Поле 'entry_point' должно быть непустой строкой")
        entry_point = entry_point.strip()

        entry_point_path = (base_dir / entry_point).resolve()
        try:
            entry_point_path.relative_to(base_dir.resolve())
        except ValueError:
            raise ValueError(f"Небезопасный путь entry_point '{entry_point}': выходит за пределы каталога игры")

        if not entry_point_path.is_file():
            raise FileNotFoundError(f"Файл запуска '{entry_point}' не найден в {base_dir}")

        version = str(data.get("version", "1.0.0"))
        icon = str(data.get("icon", PLACEHOLER_ICON))

        if not icon.strip():
            icon = PLACEHOLER_ICON

        return cls(
            name=name,
            author=author,
            description=description,
            icon=icon,
            entry_point=entry_point,
            version=version,
        )


class Game:
    def __init__(self, path: Path, metadata: GameMetadata) -> None:
        self.path = path
        self.metadata = metadata

        self.name = metadata.name
        self.author = metadata.author
        self.description = metadata.description
        self.icon = metadata.icon
        self.version = metadata.version
        self.entry_point = metadata.entry_point

    def launch(self) -> None:
        entry_file = self.path / self.entry_point
        if not entry_file.is_file():
            logger.error(f"Не удалось запустить игру '{self.name}': файл {entry_file} не найден")
            return

        try:
            logger.info(f"Запуск игры: {self.name} ({entry_file})")
            subprocess.Popen([sys.executable, str(entry_file.name)], cwd=str(self.path.resolve()))
        except Exception as e:
            logger.error(f"Ошибка при запуске игры '{self.name}': {e}")


def create_placeholder_icon(size: int, label: str = "?") -> pygame.Surface:
    """Создает запасную иконку-заглушку, если картинка не найдена или повреждена."""
    surface = pygame.Surface((size, size))
    surface.fill((70, 70, 70))
    pygame.draw.rect(surface, (100, 100, 100), surface.get_rect(), width=3, border_radius=8)

    try:
        font = pygame.font.SysFont("Arial", size // 2, bold=True)
        text = font.render(label, True, (200, 200, 200))
        text_rect = text.get_rect(center=(size // 2, size // 2))
        surface.blit(text, text_rect)
    except Exception:
        pass

    return surface


def load_game_icon(game_path: Path, icon_rel_path: str, size: int) -> pygame.Surface:
    """Безопасно загружает и масштабирует иконку игры с защитой от ошибок и падений."""
    if not icon_rel_path or icon_rel_path == PLACEHOLER_ICON:
        return create_placeholder_icon(size)

    icon_path = (game_path / icon_rel_path).resolve()
    try:
        icon_path.relative_to(game_path.resolve())
    except ValueError:
        logger.warning(f"Путь к иконке '{icon_rel_path}' выходит за пределы каталога игры")
        return create_placeholder_icon(size)

    if not icon_path.is_file():
        logger.warning(f"Файл иконки не найден: {icon_path}")
        return create_placeholder_icon(size)

    try:
        raw_image = pygame.image.load(str(icon_path))
        return pygame.transform.scale(raw_image, (size, size))
    except Exception as e:
        logger.warning(f"Не удалось загрузить изображение иконки '{icon_path}': {e}")
        return create_placeholder_icon(size)


def truncate_text(text: str, font: pygame.font.Font, max_width: int) -> str:
    """Обрезает строку с добавлением '...', если она превышает ширину max_width."""
    if font.size(text)[0] <= max_width:
        return text

    ellipsis = "..."
    ellipsis_width = font.size(ellipsis)[0]
    while text and font.size(text)[0] + ellipsis_width > max_width:
        text = text[:-1]

    return text.strip() + ellipsis


def wrap_text(text: str, font: pygame.font.Font, max_width: int, max_lines: int = 3) -> list[str]:
    """Разбивает текст на несколько строк с учетом ограничения по ширине и числу строк."""
    words = text.split()
    lines: list[str] = []
    current_line = ""

    for word in words:
        test_line = f"{current_line} {word}".strip()
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
                if len(lines) == max_lines:
                    break
            current_line = word

    if current_line and len(lines) < max_lines:
        lines.append(current_line)

    if len(lines) == max_lines and words:
        lines[-1] = truncate_text(lines[-1], font, max_width)

    return lines


class Card:
    ICON_SIZE = 250
    INDENT = 25
    FONT_NAME = "Arial"
    NAME_FONT_SIZE = 36
    AUTHOR_FONT_SIZE = 22
    DESCRIPTION_FONT_SIZE = 16
    TEXT_COLOR = (255, 255, 255)
    AUTHOR_COLOR = (180, 180, 180)
    DESC_COLOR = (220, 220, 220)
    CARD_COLOR = (50, 50, 50)
    CARD_HOVER_COLOR = (80, 80, 80)

    def __init__(self, rect: pygame.Rect, game: Game) -> None:
        self.game = game
        self.rect = rect
        self.name = game.name
        self.author = game.author
        self.description = game.description
        self.card_color = self.CARD_COLOR
        self.icon_image = load_game_icon(game.path, game.icon, self.ICON_SIZE)

    def draw(self, screen: pygame.Surface) -> None:
        # Оптимизировать создание текста и шрифтов
        pygame.draw.rect(screen, self.card_color, self.rect, border_radius=10)

        screen.blit(self.icon_image, (self.rect.x + self.INDENT, self.rect.y + self.INDENT))

        max_text_width = self.rect.width - 2 * self.INDENT
        rect_center_x = self.rect.centerx

        name_font = pygame.font.SysFont(self.FONT_NAME, self.NAME_FONT_SIZE, bold=True)
        display_name = truncate_text(self.name, name_font, max_text_width)
        name_surf = name_font.render(display_name, True, self.TEXT_COLOR)
        name_rect = name_surf.get_rect(center=(rect_center_x, self.rect.y + 310))
        screen.blit(name_surf, name_rect)

        author_font = pygame.font.SysFont(self.FONT_NAME, self.AUTHOR_FONT_SIZE)
        display_author = truncate_text(f"by {self.author}", author_font, max_text_width)
        author_surf = author_font.render(display_author, True, self.AUTHOR_COLOR)
        author_rect = author_surf.get_rect(center=(rect_center_x, self.rect.y + 350))
        screen.blit(author_surf, author_rect)

        desc_font = pygame.font.SysFont(self.FONT_NAME, self.DESCRIPTION_FONT_SIZE)
        desc_lines = wrap_text(self.description, desc_font, max_text_width, max_lines=4)
        start_y = self.rect.y + 385
        line_height = desc_font.get_linesize()

        for i, line in enumerate(desc_lines):
            line_surf = desc_font.render(line, True, self.DESC_COLOR)
            line_rect = line_surf.get_rect(center=(rect_center_x, start_y + i * line_height))
            screen.blit(line_surf, line_rect)

    def handle_mouse(self, event: pygame.event.Event):
        self.card_color = self.CARD_COLOR

        if self.rect.collidepoint(event.pos):
            if event.type == pygame.MOUSEMOTION:
                self.card_color = self.CARD_HOVER_COLOR

            elif event.type == pygame.MOUSEBUTTONUP:
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
        self.scroll_y = 0

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Pygame Collab")

    def discover_games(self) -> list[Game]:
        games = []

        if not GAMES_DIR.exists():
            logger.warning(f"Папка с играми '{GAMES_DIR}' не существует")
            return games

        for path in sorted(GAMES_DIR.iterdir()):
            if not path.is_dir():
                continue

            metadata_path = path / "metadata.json"
            if not metadata_path.exists():
                logger.info(f"Пропуск каталога '{path.name}': отсутствует metadata.json")
                continue

            try:
                raw_content = metadata_path.read_text(encoding="utf-8")
            except Exception as e:
                logger.error(f"Не удалось прочитать файл {metadata_path}: {e}")
                continue

            try:
                raw_data = json.loads(raw_content)
            except json.JSONDecodeError as e:
                logger.error(f"Ошибка синтаксиса JSON в {metadata_path}: {e}")
                continue

            try:
                metadata = GameMetadata.from_dict(raw_data, base_dir=path)
                games.append(Game(path, metadata))
                logger.info(f"Успешно загружена игра: {metadata.name} ({path.name})")
            except Exception as e:
                logger.error(f"Ошибка валидации игры в '{path.name}': {e}")

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

    def check_card_mouse(self, event: pygame.event.Event) -> None:
        for card in self.cards:
            if card.handle_mouse(event):
                pygame.event.clear()
                break

    def handle_mouse_wheel(self, event: pygame.event.Event):
        for card in self.cards:
            card.rect.move_ip(0, event.y * SCROLL_SPEED)

    def handle_events(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.check_card_mouse(event)
            elif event.type == pygame.MOUSEMOTION:
                self.check_card_mouse(event)
            elif event.type == pygame.MOUSEWHEEL:
                self.handle_mouse_wheel(event)

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